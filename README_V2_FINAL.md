# ALT F4 Jardineiro AI — V2 FINAL

Esta versão está preparada para virar uma aplicação Windows autónoma.

## O que mudou
- Dados guardados numa pasta própria em `%LOCALAPPDATA%\ALT_F4_Jardineiro_AI`.
- Interface mais simples.
- F8 grava, F9 guarda, F10 para.
- Melhor tratamento de erros.
- Configuração de PyInstaller incluída.
- Script `CRIAR_EXE_WINDOWS.bat` para criar o `.exe`.

## Importante
O ZIP contém o projeto e o processo de criação do `.exe`. A criação final do executável Windows tem de ser feita num Windows (ou num serviço de build Windows), porque este ambiente não executa o empacotamento Windows diretamente.

Depois de criar o EXE, o ficheiro será:
`dist\ALT_F4_Jardineiro_AI.exe`

A partir daí, o objetivo é usar o EXE sem Python, sem CMD e sem instalar dependências manualmente.
