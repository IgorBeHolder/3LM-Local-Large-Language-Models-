# LLM_MVP

## Description
Требования:
1. Оффлайновый инференс моделей на базе архитектур Llama / Llama-2 (обязательно) и других архитектур (GPT-J, MPT и так далее) - желательно
1. Возможность инференса как на GPU, так и на CPU, поддержка квантированных моделей в обоих режимах
1. Поддержка LoRa / QLoRA-адаптеров, желательно раздельно с базовой моделью, т.е. возможность загрузить базовую модель в память один раз и разным пользователям обращаться к ней через разные адаптеры, при этом хранить адаптеры отдельно от модели
1. Возможность создания своих адаптеров через файн-тюн путём загрузки CSV с примерами prompt и response
1. RESTful API для внешних систем совместимый с OpenAI API - для инференса и для эмбеддингов и с поддержкой одновременных конкурентных запросов. Для GPU-инференса поддержка автоматического батчинга запросов, для CPU-инференса как минимум поддержка постановки запросов в очередь, или желательно распараллеливание на доступных ядрах/ресурсах

# Flask-OpenLLM MVP

A template for an MVP integrating Flask and OpenLLM.

## Setup
1. Create a virtual environment: `python3 -m venv venv`
2. Activate it: `source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows)
(3. Install requirements: `pip install -r dev.txt`)
4. Run the app: `docker compose -p postgres_container -f ./docker/docker-compose.yml up --build`

## Features
- [ ] Model loading and management with OpenLLM.
- [ ] Custom adapters support.
... (and so on)

## Available openAI models
```bash
curl https://api.openai.com/v1/models   -H "Authorization: Bearer $(grep OPENAI_API_KEY .env | cut -d= -f2)" > models.txt
```  

