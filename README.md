A plataforma roda em docker e em desenvolvimento no virtual environment.


Para rodar em desenvolvimento você precisa ter instalado um virtual environment com Python v.3.10 ou acima.


## ✨ Como startar a plataforma

> **Passo 1** Baixe o código

```bash
$ git clone https://github.com/app-generator/django-volt-dashboard.git
```

<br />

### 👉 Preparar para desenvolvimento em `Linux` 

> **Passo 2** Crie um virtual environment e instale os modulos  

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
``` 



<br />

> **Step 3** - De start na Plataforma

```bash
$ dev=True ./manage.py runserver 
```

Visite `http://localhost:8000` no seu navegador, a plataforma deve estar rodando. <br />

<br />

