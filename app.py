"""
Flask Web Application for Brasileirão Players Search
Mobile-first responsive design with Bootstrap
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import requests
from datetime import datetime
from typing import Optional, List, Dict
import re

app = Flask(__name__)

# Configuração de sessão
app.secret_key = 'sua_chave_secreta_aqui_mude_em_producao'  # MUDE EM PRODUÇÃO!

# API base URL - pode ser ajustado para produção
API_BASE_URL = "http://localhost:8000"

class APIClient:
    """Cliente para comunicação com a API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._players_cache = None  # Cache dos jogadores
        self._cache_timestamp = None
        
    def _load_all_players(self):
        """Carrega todos os jogadores da API e mantém em cache"""
        try:
            # Cache válido por 5 minutos
            import time
            current_time = time.time()
            if (self._players_cache is not None and 
                self._cache_timestamp is not None and 
                current_time - self._cache_timestamp < 300):
                return self._players_cache
            
            print("🔄 Carregando todos os jogadores da API...")
            all_players = []
            
            # Carrega jogadores em páginas
            offset = 0
            page_size = 1000
            
            while True:
                params = {"limit": page_size, "offset": offset}
                response = requests.get(f"{self.base_url}/players", params=params, timeout=10)
                if response.status_code == 200:
                    players = response.json()
                    if not players:
                        break
                    all_players.extend(players)
                    if len(players) < page_size:
                        break
                    offset += page_size
                else:
                    print(f"❌ Erro ao carregar jogadores: {response.status_code}")
                    break
            
            self._players_cache = all_players
            self._cache_timestamp = current_time
            print(f"✅ Carregados {len(all_players)} jogadores no cache")
            return all_players
            
        except Exception as e:
            print(f"❌ Erro ao carregar todos os jogadores: {e}")
            return []
    
    def search_players_local(self, name: Optional[str] = None, position: Optional[str] = None,
                           serie: Optional[str] = None, club: Optional[str] = None,
                           age_min: Optional[int] = None, age_max: Optional[int] = None) -> List[Dict]:
        """Busca local nos dados carregados da API"""
        try:
            # Carrega todos os jogadores
            all_players = self._load_all_players()
            filtered = all_players.copy()
            
            print(f"🔍 Iniciando busca local com {len(filtered)} jogadores")
            
            # Filtro por nome (busca parcial, case-insensitive)
            if name and name.strip():
                name_lower = name.strip().lower()
                filtered = [p for p in filtered if name_lower in p.get("name", "").lower()]
                print(f"📝 Filtro por nome '{name}': {len(filtered)} jogadores")
            
            # Filtro por posição
            if position and position.strip():
                filtered = [p for p in filtered if p.get("position") == position.strip()]
                print(f"⚽ Filtro por posição '{position}': {len(filtered)} jogadores")
            
            # Filtro por série
            if serie and serie.strip():
                filtered = [p for p in filtered if p.get("serie") == serie.strip()]
                print(f"🏆 Filtro por série '{serie}': {len(filtered)} jogadores")
            
            # Filtro por clube
            if club and club.strip():
                filtered = [p for p in filtered if p.get("club_name") == club.strip()]
                print(f"🛡️ Filtro por clube '{club}': {len(filtered)} jogadores")
            
            # Filtro por idade mínima
            if age_min is not None:
                filtered = [p for p in filtered if p.get("age") is not None and p.get("age") >= age_min]
                print(f"📅 Filtro idade mínima {age_min}: {len(filtered)} jogadores")
            
            # Filtro por idade máxima
            if age_max is not None:
                filtered = [p for p in filtered if p.get("age") is not None and p.get("age") <= age_max]
                print(f"📅 Filtro idade máxima {age_max}: {len(filtered)} jogadores")
            
            print(f"✅ Busca local finalizada: {len(filtered)} jogadores encontrados")
            return filtered
            
        except Exception as e:
            print(f"❌ Erro na busca local: {e}")
            return []
        
    def get_players(self, limit: int = 100, offset: int = 0, serie: Optional[str] = None, 
                   club: Optional[str] = None, position: Optional[str] = None) -> List[Dict]:
        """Busca jogadores - agora usa busca local"""
        return self.search_players_local(
            serie=serie, 
            club=club, 
            position=position
        )[offset:offset + limit]
    
    def search_players(self, name: Optional[str] = None, position: Optional[str] = None,
                      serie: Optional[str] = None, club: Optional[str] = None,
                      age_min: Optional[int] = None, age_max: Optional[int] = None,
                      limit: int = 100) -> List[Dict]:
        """Busca avançada de jogadores - agora usa busca local"""
        try:
            results = self.search_players_local(
                name=name,
                position=position,
                serie=serie,
                club=club,
                age_min=age_min,
                age_max=age_max
            )
            return results[:limit] if limit else results
        except Exception as e:
            print(f"❌ Erro na busca avançada: {e}")
            return []
    
    def get_player_profile(self, player_id: str) -> Optional[Dict]:
        """Busca perfil de um jogador específico"""
        try:
            response = requests.get(f"{self.base_url}/players/{player_id}/profile", timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erro ao buscar perfil do jogador {player_id}: {e}")
            return None
    
    def get_player_stats(self, player_id: str) -> Optional[Dict]:
        """Busca estatísticas de um jogador"""
        try:
            response = requests.get(f"{self.base_url}/players/{player_id}/stats", timeout=15)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erro ao buscar estatísticas do jogador {player_id}: {e}")
            return None
    
    def get_series_info(self) -> List[Dict]:
        """Busca informações das séries a partir dos jogadores carregados"""
        try:
            players = self._load_all_players()
            series_count = {}
            
            for player in players:
                serie = player.get("serie", "Sem Série")
                series_count[serie] = series_count.get(serie, 0) + 1
            
            # Retorna no formato esperado
            series_info = []
            for serie, count in sorted(series_count.items()):
                series_info.append({
                    "name": serie,
                    "players_count": count
                })
            
            return series_info
        except Exception as e:
            print(f"Erro ao buscar séries: {e}")
            return []
    
    def get_clubs_info(self, serie: Optional[str] = None) -> List[Dict]:
        """Busca informações dos clubes a partir dos jogadores carregados"""
        try:
            players = self._load_all_players()
            clubs_count = {}
            
            for player in players:
                # Filtra por série se especificado
                if serie and player.get("serie") != serie:
                    continue
                    
                club = player.get("club_name", "Sem Clube")
                if club not in clubs_count:
                    clubs_count[club] = {
                        "name": club,
                        "serie": player.get("serie", ""),
                        "players_count": 0
                    }
                clubs_count[club]["players_count"] += 1
            
            # Retorna lista ordenada
            return sorted(clubs_count.values(), key=lambda x: x["name"])
        except Exception as e:
            print(f"Erro ao buscar clubes: {e}")
            return []

# Cliente da API
api_client = APIClient(API_BASE_URL)

def parse_date(date_str: str) -> Optional[datetime]:
    """Converte string de data para datetime"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        try:
            return datetime.strptime(date_str, "%d/%m/%Y")
        except:
            return None

def format_currency(value: str) -> str:
    """Formata valor monetário no formato abreviado (7M, 700k, etc.)"""
    if not value or value == "N/A" or value is None:
        return "N/A"
    
    # Garantir que é string
    value_str = str(value).strip()
    
    # Se já está no formato abreviado, retorna como está
    if any(suffix in value_str.upper() for suffix in ['M', 'K']) and len(value_str) <= 10:
        return value_str
    
    # Extrai valor numérico do texto
    try:
        # Remove símbolos de moeda e espaços
        clean_value = re.sub(r'[€$£R\s]', '', value_str)
        
        # Substitui vírgulas por pontos para números decimais
        clean_value = clean_value.replace(',', '.')
        
        # Extrai apenas números e pontos
        numeric_match = re.search(r'[\d.]+', clean_value)
        if not numeric_match:
            return value_str
            
        numeric_value = float(numeric_match.group())
        
        # Formato abreviado
        if numeric_value >= 1000000:
            # Milhões
            millions = numeric_value / 1000000
            if millions >= 10:
                return f"{int(millions)}M"
            else:
                return f"{millions:.1f}M".rstrip('0').rstrip('.')
        elif numeric_value >= 1000:
            # Milhares
            thousands = numeric_value / 1000
            if thousands >= 10:
                return f"{int(thousands)}k"
            else:
                return f"{thousands:.0f}k"
        else:
            # Valores menores que 1000
            return f"{int(numeric_value)}" if numeric_value == int(numeric_value) else f"{numeric_value:.1f}"
            
    except (ValueError, TypeError):
        return value_str if value_str else "N/A"
    
    return value_str if value_str else "N/A"

def calculate_age(birth_date: str) -> Optional[int]:
    """Calcula idade a partir da data de nascimento"""
    if not birth_date:
        return None
    birth = parse_date(birth_date)
    if birth:
        today = datetime.now()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    return None

# Configurações de login simples


def is_logged_in():
    """Verifica se o usuário está logado"""
    return session.get('logged_in', False)

def require_login(f):
    """Decorator para rotas que requerem login"""
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            session['username'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout do usuário"""
    session.clear()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('login'))

@app.route('/')
@require_login
def index():
    """Página principal com busca de jogadores"""
    # Busca parâmetros da URL
    search_name = request.args.get('search_name', '')
    serie_filter = request.args.get('serie', '')
    club_filter = request.args.get('club', '')
    position_filter = request.args.get('position', '')
    age_min = request.args.get('age_min', type=int)
    age_max = request.args.get('age_max', type=int)
    sort_by = request.args.get('sort_by', 'name')
    page = request.args.get('page', 1, type=int)
    
    # Busca dados
    series_info = api_client.get_series_info()
    clubs_info = api_client.get_clubs_info()
    
    # Busca jogadores com sistema local
    players = []
    
    # Se há qualquer filtro ativo, usa busca avançada local
    if any([search_name, serie_filter, club_filter, position_filter, age_min, age_max]):
        players = api_client.search_players(
            name=search_name.strip() if search_name else None,
            serie=serie_filter if serie_filter else None,
            club=club_filter if club_filter else None,
            position=position_filter if position_filter else None,
            age_min=age_min,
            age_max=age_max,
            limit=None  # Sem limite para permitir ordenação completa
        )
        print(f"✅ Busca com filtros retornou {len(players)} jogadores")
    else:
        # Busca padrão - todos os jogadores
        players = api_client._load_all_players()
        print(f"✅ Busca padrão retornou {len(players)} jogadores")

    # Processar idades
    for player in players:
        player['calculated_age'] = calculate_age(player.get('dateOfBirth'))

    # Filtro por expiração do contrato (em meses)
    contract_end_filter = request.args.get('contract_end')
    if contract_end_filter:
        try:
            months = int(contract_end_filter)
            from datetime import datetime, timedelta
            
            # Calcula a data limite baseada nos meses selecionados
            today = datetime.now()
            limit_date = today + timedelta(days=months * 30)  # Aproximação de 30 dias por mês
            
            print(f"📅 Filtro contrato: contratos que expiram em até {months} meses (até {limit_date.strftime('%d/%m/%Y')})")
            
            # Debug: verificar alguns contratos
            contracts_found = 0
            contracts_samples = []
            
            filtered_players = []
            for player in players:
                # Verifica diferentes formatos possíveis de contrato
                contract_data = player.get('contract')
                contract_end_date = None
                
                if isinstance(contract_data, dict):
                    # Formato: {"until": "data"}
                    contract_end_date = parse_date(contract_data.get('until'))
                elif isinstance(contract_data, str):
                    # Formato: string com data direta
                    contract_end_date = parse_date(contract_data)
                
                # Também verifica se há campo direto
                if not contract_end_date:
                    contract_end_date = parse_date(player.get('contractUntil') or player.get('contract_until'))
                
                if contract_end_date:
                    contracts_found += 1
                    if len(contracts_samples) < 5:
                        contracts_samples.append(f"{player.get('name', 'N/A')}: {contract_end_date.strftime('%d/%m/%Y')}")
                    
                    if contract_end_date <= limit_date:
                        filtered_players.append(player)
            
            print(f"📋 Total de contratos encontrados: {contracts_found}")
            print(f"📝 Exemplos: {contracts_samples[:3]}")
            print(f"🎯 Jogadores com contrato expirando em {months} meses: {len(filtered_players)}")
            
            players = filtered_players
            
        except (ValueError, TypeError) as e:
            print(f"⚠️ Erro no filtro de contrato: {e}")
            pass
    
    # Ordenação melhorada (similar ao Flet)
    def sort_key(player):
        if sort_by == 'name':
            return player.get('name', '').lower()
        elif sort_by == 'age':
            return player.get('age') or player.get('calculated_age') or 999
        elif sort_by == 'market_value' or sort_by == 'marketValue':
            # Extrai valor numérico do market value
            mv = player.get('marketValue', 0)
            if isinstance(mv, (int, float)):
                return mv
            # Se for string, tenta converter
            if mv and mv != 'N/A':
                numeric = re.sub(r'[^\d.,]', '', str(mv).replace(',', '.'))
                try:
                    return float(numeric)
                except:
                    return 0
            return 0
        elif sort_by == 'contract_end' or sort_by == 'contract':
            contract_date = player.get('contract')
            if contract_date:
                try:
                    return datetime.strptime(contract_date, "%Y-%m-%d")
                except:
                    return datetime.max
            return datetime.max
        elif sort_by == 'position':
            return player.get('position', '').lower()
        elif sort_by == 'club_name' or sort_by == 'club':
            return player.get('club_name', '').lower()
        elif sort_by == 'serie':
            return player.get('serie', '').lower()
        return player.get('name', '').lower()

    # Aplica ordenação
    reverse_order = request.args.get('order', 'asc') == 'desc'
    players.sort(key=sort_key, reverse=reverse_order)
    
    # Agrupa jogadores por série primeiro
    players_by_series = {}
    for player in players:
        serie = player.get('serie', 'Outros')
        if serie not in players_by_series:
            players_by_series[serie] = []
        players_by_series[serie].append(player)
    
    # Limite de jogadores por série (25) antes da paginação
    max_per_series = 25
    
    # Aplica limite por série e depois faz paginação global
    limited_players = []
    for serie in ['Série A', 'Série B', 'Série C', 'Série D']:
        if serie in players_by_series:
            serie_players = players_by_series[serie][:max_per_series]
            limited_players.extend(serie_players)
    
    # Adiciona outras séries (se houver)
    for serie, serie_players in players_by_series.items():
        if serie not in ['Série A', 'Série B', 'Série C', 'Série D']:
            limited_players.extend(serie_players[:max_per_series])
    
    # Paginação sobre os jogadores limitados
    per_page = 100  # Aumenta per_page já que limitamos por série
    total_players = len(limited_players)
    total_pages = (total_players + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    players_page = limited_players[start_idx:end_idx]
    
    # Reagrupa para exibição final
    players_by_series = {}
    
    # Define ordem prioritária das séries principais
    main_series = ['Série A', 'Série B', 'Série C', 'Série D']
    
    # Inicializa séries principais (mesmo que vazias)
    for serie in main_series:
        players_by_series[serie] = []
    
    # Agrupa jogadores por série
    for player in players_page:
        serie = player.get('serie', 'Outras Séries')
        
        # Normaliza nome da série
        if 'série a' in serie.lower() or serie.lower() == 'a':
            serie = 'Série A'
        elif 'série b' in serie.lower() or serie.lower() == 'b':
            serie = 'Série B'
        elif 'série c' in serie.lower() or serie.lower() == 'c':
            serie = 'Série C'
        elif 'série d' in serie.lower() or serie.lower() == 'd':
            serie = 'Série D'
        
        if serie not in players_by_series:
            players_by_series[serie] = []
        players_by_series[serie].append(player)
    
    # Remove séries vazias (exceto as principais)
    players_by_series = {
        serie: players for serie, players in players_by_series.items() 
        if len(players) > 0 or serie in main_series
    }
    
    return render_template('index.html',
                         players_by_series=players_by_series,
                         series_info=series_info,
                         clubs_info=clubs_info,
                         search_params={
                             'search_name': search_name,
                             'serie': serie_filter,
                             'club': club_filter,
                             'position': position_filter,
                             'age_min': age_min,
                             'age_max': age_max,
                             'sort_by': sort_by,
                             'contract_end': contract_end_filter
                         },
                         pagination={
                             'page': page,
                             'total_pages': total_pages,
                             'total_players': total_players,
                             'per_page': per_page
                         })

@app.route('/player/<player_id>')
@require_login
def player_profile(player_id):
    """Página de perfil do jogador"""
    # Busca perfil e estatísticas
    profile = api_client.get_player_profile(player_id)
    stats = api_client.get_player_stats(player_id)
    
    if not profile:
        return render_template('error.html', message="Jogador não encontrado"), 404
    
    # Adiciona idade calculada
    profile['calculated_age'] = calculate_age(profile.get('dateOfBirth'))
    
    return render_template('player_profile.html', 
                         profile=profile, 
                         stats=stats)

@app.route('/api/clubs/<serie>')
def api_clubs_by_serie(serie):
    """API endpoint para buscar clubes por série (para AJAX)"""
    clubs = api_client.get_clubs_info(serie=serie)
    return jsonify([club['name'] for club in clubs])

@app.template_filter('format_date')
def format_date(date_str):
    """Filtro para formatação de datas"""
    if not date_str:
        return "N/A"
    date_obj = parse_date(date_str)
    if date_obj:
        return date_obj.strftime("%d/%m/%Y")
    return date_str

@app.template_filter('format_currency')
def format_currency_filter(value):
    """Filtro para formatação de moeda"""
    return format_currency(value)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
