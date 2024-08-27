
# 🗓️ Gerador de Escala de Trabalho - Shopping Iguatemi

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/seu-usuario/gerador-escala-iguatemi)

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Começando](#-começando)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação](#instalação)
- [Uso](#-uso)
- [Personalização](#-personalização)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Contribuindo](#-contribuindo)
- [Versionamento](#-versionamento)
- [Autores](#-autores)
- [Licença](#-licença)
- [Agradecimentos](#-agradecimentos)

## 🚀 Sobre o Projeto

O **Gerador de Escala de Trabalho** é uma ferramenta automatizada desenvolvida em Python, projetada para atender às necessidades de gerenciamento de pessoal do Shopping Iguatemi. Ele cria escalas mensais eficientes, considerando fatores como múltiplos turnos, rotações de domingo e folgas semanais, garantindo uma distribuição justa e otimizada dos horários de trabalho.

## ✨ Funcionalidades

- **Geração de escalas mensais personalizadas**
- **Suporte a múltiplos turnos de trabalho** (10h às 18h, 14h às 22h)
- **Implementação de rotações de domingo** e escalas de vendedores
- **Cálculo e exibição de estatísticas por funcionário** (dias trabalhados, domingos)
- **Exportação da escala em formato Excel** com formatação visual aprimorada
- **Estilização automática para fácil visualização** (cores por turno, destaque para domingos)

## 🛠 Tecnologias Utilizadas

- [Python](https://www.python.org/) - Linguagem de programação principal
- [pandas](https://pandas.pydata.org/) - Manipulação e análise de dados
- [openpyxl](https://openpyxl.readthedocs.io/) - Criação de arquivos Excel
- [calendar](https://docs.python.org/3/library/calendar.html) - Manipulação de datas

## 🏁 Começando

Siga as instruções abaixo para configurar o projeto em sua máquina local para fins de desenvolvimento e testes.

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/gerador-escala-iguatemi.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd gerador-escala-iguatemi
   ```

3. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```

## 📋 Uso

1. Abra o arquivo `escala_iguatemi.py` em seu editor de código preferido.

2. Modifique as variáveis de configuração conforme necessário:
   ```python
   employees = {...}  # Dicionário de funcionários
   sunday_rotation = [...]  # Lista de rotações de domingo
   vendor_rotation = [...]  # Lista de rotações de vendedores
   weekdays_off = {...}  # Dicionário de folgas semanais 
   ```

3. Execute o script para gerar a escala. O arquivo Excel será salvo no diretório do projeto.

## 🔧 Personalização

- **Funcionários**: Adicione ou remova funcionários no dicionário `employees`.
- **Rotações**: Ajuste `sunday_rotation` e `vendor_rotation` para modificar as escalas de domingo.
- **Folgas**: Altere `weekdays_off` para definir os dias de folga de cada funcionário.
- **Período**: Modifique as variáveis `year` e `month` para gerar a escala de um período específico.

## 📁 Estrutura do Projeto

```plaintext
gerador-escala-iguatemi/
│
├── escala_iguatemi.py    # Script principal
├── requirements.txt      # Dependências do projeto
├── README.md             # Este arquivo
└── LICENSE               # Licença do projeto
```

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Para contribuir, siga os passos abaixo:

1. Faça um Fork do projeto.
2. Crie uma Branch para sua feature (`git checkout -b feature/AmazingFeature`).
3. Faça commit das suas mudanças (`git commit -m 'Add some AmazingFeature'`).
4. Faça push para a Branch (`git push origin feature/AmazingFeature`).
5. Abra um Pull Request.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](./LICENSE) para detalhes.

## 🙏 Agradecimentos

Agradecemos a todos os colaboradores e desenvolvedores que contribuíram para este projeto.