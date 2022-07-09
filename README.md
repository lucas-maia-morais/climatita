# [Climatita](https://climatita-exame.herokuapp.com/)
 - O [Climatita](https://climatita-exame.herokuapp.com/) faz uma projeção do tempo a partir da localização dada, dando dicas ao usuário a depender do clima local!.
 - O sistema implementa o CRUD e filtros para melhorar a busca do usuário.
 - Link para o [site]([Climatita](https://climatita-exame.herokuapp.com/))

## Sumário
 - Nos próximos seções poderemos ver o resultado final
 - A seguir veremos os detalhes sobre as funcionalides do Climatita.

## Visão geral
 - Aqui podemos ver o primeiro layout onde podemos escolher as cidades, por temperatura, descrição, dica da hora e ações.

## Instalação:

### Servidor
Inicialmente vamos realizar a instalação seguindo o passo a passo com as bibliotecas necessárias de Python. A versão utilizada para o python foi a 3.7.11.

```
pip install flask
pip install googletrans==3.1.0a0
pip install requests
pip install flask_sqlalchemy
pip install flask_cors
```
Para rodar:
```
flask run
```

### Cliente/Front-end
Foi utilizada a tecnologia Vue para implementar o front-end da aplicação. Para isso devemos segue abaixo um passo a passo para instalação:
```
sudo npm install -g @vue/cli@4.5.11
```

Para rodar:
```
npm run serve
```

## Funcionalidades

### Adicionando cidades
 - Clicando em "Adicionar cidade" podemos ver no exemplo: "São José dos Campos, BR; 23°; scattered clouds (nuvens espalhadas); dica da hora: Aproveite o dia para caminhar, a temperatura está ótima; e Ações: Mostrar, Atualizar ou Deletar"
 - Ao clicar em "Adicionar cidade", como destacado na imagem anterior, o seguinte display aparece para o usuário: "Adicione uma nova cidade; Cidade; Submit / Reset".

### Como fica após adicionar algumas cidades?
 - Como pode-se ver pela imagem, adicionando cidades de interesse, a temperatura, descrição meterológica e dicas de acordo com o clima local aparecerão para o usuário.

### Funcionalidades
 - Após adicionar as cidades ao banco de dados, é interessante sempre usar quando necessário os botões indicados na figura: atualizar ou deletar.
 - Além dos botões "atualizar" e "deletar", temos o "mostrar" que tem a função de detalhar numa seção separada as informações sobre a cidade selecionada como mostra a figura.
