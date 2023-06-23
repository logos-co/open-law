# Open-Law

# Installation

1. Create virtual environment and install dependencies `poetry install`
2. Install node packages `yarn`
3. Run webpack JS bundler `yarn js-watch`
4. Run webpack CSS bundler `yarn css-watch`
5. Rename `project.env` to `.env`
6. Up docker container with database `docker-compose up -d db`
7. Apply migrations `flask db upgrade`
8. Run project in the vs-code debugger `F5`

# Build

1. To minify static files run `yarn js` and `yarn css` or `sh build_static.sh`
2. Build docker containers `docker-compose build`
3. Run docker containers `docker-compose up -d`

### To set up auto deployment CI/CD you need to set following variables in the Actions secrets and variables page of repository settings

`DOCKERHUB_TOKEN` - hub.docker.com api token
`DOCKERHUB_USERNAME` - hub.docker.com username
`SSH_HOST_IP_PROD` - VPS IP
`SSH_KEY` - VPS ssh key
`SSH_USER` - VPS user
