# 🌐 Brasileirão Players Search - Website Flask

Um site web responsivo e mobile-first construído com Flask e Bootstrap para visualizar e buscar jogadores do Brasileirão.

## ✨ Características

### 🎯 **Funcionalidades Principais**
- **Busca Avançada**: Nome, posição, série, clube, idade e data de expiração do contrato
- **Perfil Detalhado**: Informações completas e estatísticas em tempo real
- **Ordenação**: Por nome, idade, valor de mercado e data de contrato
- **Filtros Dinâmicos**: Clubes carregados automaticamente por série
- **Paginação**: Navegação eficiente para grandes volumes de dados

### 📱 **Design Mobile-First**
- **Responsivo**: Bootstrap 5 com design adaptável
- **Touch-friendly**: Otimizado para dispositivos touch
- **Performance**: Carregamento rápido e navegação fluida
- **Acessibilidade**: Suporte completo a leitores de tela

### 🎨 **Interface Moderna**
- **Cards visuais**: Layout limpo e organizado
- **Navegação por séries**: Separação visual clara
- **Estatísticas detalhadas**: Tabs por temporada
- **Feedback visual**: Toast notifications e loading states

## 🚀 Instalação e Execução

### 1️⃣ **Pré-requisitos**
```bash
# Certifique-se de que a API está rodando
cd /Users/artur/Projects/Python/PlayersSearch/tf-api/api
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2️⃣ **Instalação**
```bash
cd /Users/artur/Projects/Python/PlayersSearch/tf-api/flask_site

# Instalar dependências
pip3 install -r requirements.txt
```

### 3️⃣ **Execução**
```bash
# Executar o site Flask
python3 app.py
```

O site estará disponível em: **http://localhost:5000**

## 📂 Estrutura do Projeto

```
flask_site/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── README.md             # Este arquivo
├── static/               # Arquivos estáticos
│   ├── css/
│   │   └── style.css     # Estilos customizados
│   └── js/
│       └── main.js       # JavaScript customizado
└── templates/            # Templates Jinja2
    ├── base.html         # Template base
    ├── index.html        # Página principal
    ├── player_profile.html # Perfil do jogador
    ├── pagination.html   # Componente de paginação
    └── error.html        # Página de erro
```

## 🎯 Funcionalidades Detalhadas

### 🔍 **Busca de Jogadores**
- **Busca por nome**: Busca parcial e case-insensitive
- **Filtros por categoria**: Série, clube, posição
- **Intervalo de idade**: Idade mínima e máxima
- **Data de contrato**: Busca por jogadores com contrato expirando até uma data específica
- **Ordenação flexível**: Nome, idade, valor de mercado, data de contrato

### 👤 **Perfil do Jogador**
- **Informações pessoais**: Data de nascimento, local, nacionalidade, altura, pé
- **Informações profissionais**: Posição, valor de mercado, detalhes do contrato
- **Estatísticas em tempo real**: Dados da TransferMarkt API
- **Navegação por temporadas**: Tabs organizadas por ano
- **Ações**: Imprimir perfil, compartilhar

### 📊 **Estatísticas Detalhadas**
- **Por temporada**: Organização cronológica
- **Por competição**: Série A, Copa do Brasil, etc.
- **Métricas completas**: Jogos, minutos, gols, assistências, cartões
- **Visualização clara**: Cards organizados e coloridos

### 🎨 **Interface e Experiência**
- **Series organizadas**: Jogadores agrupados por série
- **Cards informativos**: Informações essenciais em destaque
- **Loading states**: Feedback visual durante carregamento
- **Error handling**: Mensagens claras de erro
- **Toast notifications**: Notificações não-intrusivas

## 🛠️ Tecnologias Utilizadas

### **Backend**
- **Flask 3.0**: Framework web Python moderno
- **Requests**: Cliente HTTP para comunicação com a API
- **Jinja2**: Template engine com recursos avançados

### **Frontend**
- **Bootstrap 5.3**: Framework CSS responsivo
- **Bootstrap Icons**: Ícones vetoriais
- **Vanilla JavaScript**: JavaScript puro otimizado
- **CSS Custom Properties**: Variáveis CSS para consistência

### **API Integration**
- **REST API**: Comunicação com API local (FastAPI)
- **TransferMarkt API**: Estatísticas em tempo real
- **Error handling**: Tratamento robusto de erros
- **Caching**: Cache inteligente de dados

## 📱 Compatibilidade Mobile

### **Breakpoints Responsivos**
- **Mobile**: < 576px (design otimizado)
- **Tablet**: 576px - 991px (layout adaptado)
- **Desktop**: 992px+ (experiência completa)

### **Otimizações Mobile**
- **Touch gestures**: Feedback tátil
- **Scrolling otimizado**: Performance suave
- **Campos de formulário**: Teclados específicos
- **Navegação simplificada**: Menu collapse automático

## 🔧 Configuração Avançada

### **Variáveis de Ambiente**
```python
# Em app.py, você pode configurar:
API_BASE_URL = "http://localhost:8000"  # URL da API
DEBUG = True                            # Modo debug
HOST = "0.0.0.0"                       # Host do Flask
PORT = 5000                            # Porta do Flask
```

### **Personalização de Estilos**
```css
/* Em static/css/style.css */
:root {
    --primary-color: #0066cc;    /* Cor principal */
    --border-radius: 8px;        /* Raio das bordas */
    --box-shadow: 0 2px 4px rgba(0,0,0,0.1);  /* Sombra */
}
```

## 🚀 Deploy em Produção

### **Preparação**
1. Configure variáveis de ambiente
2. Use um servidor WSGI (Gunicorn)
3. Configure proxy reverso (Nginx)
4. Ative HTTPS
5. Configure monitoramento

### **Exemplo com Gunicorn**
```bash
# Instalar Gunicorn
pip install gunicorn

# Executar em produção
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🎯 Próximos Passos

### **Melhorias Planejadas**
- [ ] Cache Redis para performance
- [ ] Autenticação de usuários
- [ ] Favoritos e listas personalizadas
- [ ] Export de dados (PDF, Excel)
- [ ] Comparação de jogadores
- [ ] Gráficos de estatísticas
- [ ] Notificações push
- [ ] PWA (Progressive Web App)

### **Otimizações Técnicas**
- [ ] Service Worker para offline
- [ ] Lazy loading de imagens
- [ ] Compressão de assets
- [ ] CDN para recursos estáticos
- [ ] Database caching
- [ ] API rate limiting

## 📧 Suporte

Para dúvidas ou problemas:
1. Verifique se a API está rodando na porta 8000
2. Confirme as dependências instaladas
3. Verifique os logs do Flask para erros
4. Teste a conectividade com a API

---

**🏆 Brasileirão Players Search - Conectando você aos dados do futebol brasileiro!**
