# llama-cpp-python-streamlit

**A streamlit app for using a llama-cpp-python high level api**

![llama-cpp-python-streamlit](https://github.com/3x3cut0r/llama-cpp-python-streamlit/assets/1408580/b22fa516-2f32-4d16-a9f2-429eee2a6f50)

## Index

1. [Installation](#install)
2. [Configuration](#config)
3. [Usage](#usage)  
   3.1 [deploy streamlit app](#deploy)  
   3.2 [use](#use)
4. [Find Me](#findme)
5. [License](#license)

## 1 Installation <a name="install"></a>

-   install python3 from [python.org](https://www.python.org/downloads/) or from repo:

```shell
apt install python3
```

-   install requirements

```shell
pip install -r requirements.txt
```

## 2 Configuration <a name="config"></a>

-   change the api url in src/config.json to your llama-cpp-python high level api
-   set your page_title to whatever you want
-   set n_ctx value to the value of your api
-   set default values to the model settings

**src/config.json**

```json
{
    "api_url": "https://llama-cpp-python.mydomain.com",
    "page_title": "Llama-2-7b-Chat",
    "n_ctx": 2048,
    "enable_context": "True",
    "stream": "True",
    "max_tokens": "256",
    "temperature": "0.2",
    "top_p": "0.95",
    "top_k": "40",
    "repeat_penalty": "1.1",
    "stop": "###",
    "system_content": "User asks Questions to the AI. AI is helpful, kind, obedient, honest, and knows its own limits.",
    "prompt": "### Instructions:\n{prompt}\n\n### Response:\n"
}
```

-   to change the logo or favicon, just replace the files inside the `./static` folder

## 3 Usage <a name="usage"></a>

### 3.1 deploy streamlit app <a name="deploy"></a>

-   run streamlit app

```shell
streamlit run streamlit_app.py
```

### 3.2 use <a name="use"></a>

-   browse [http://localhost:8501/](http://localhost:8501/)
-   choose supported endpoint
-   optional: adjust model settings/parameters
-   enter your message

### 4 Find Me <a name="findme"></a>

![E-Mail](https://img.shields.io/badge/E--Mail-julianreith%40gmx.de-red)

-   [GitHub](https://github.com/3x3cut0r)
-   [DockerHub](https://hub.docker.com/u/3x3cut0r)

### 5 License <a name="license"></a>

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) - This project is licensed under the GNU General Public License - see the [gpl-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) for details.
