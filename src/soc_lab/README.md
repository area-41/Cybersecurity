# SOC Engineering & Security Operations Study Repository

Este repositório contém anotações, laboratórios práticos e artefatos focados em Operações de Segurança (SOC), Detecção de Ameaças, Engenharia de SIEM e Automação.

## Objetivos
- Consolidar conhecimento prático e teórico sobre monitoramento e resposta a incidentes.
- Construir e versionar regras de detecção reutilizáveis (Sigma/KQL/SPL).
- Automatizar fluxos de triagem e enriquecimento de alertas.

## Trilha de Estudos
- [x] Módulo 1: Monitoramento de Tráfego e Logs
- [ ] Módulo 2: Engenharia de SIEM e Detecção de Ameaças
- [ ] Módulo 3: Governança e Métricas de SOC
- [ ] Módulo 4: Automação (SOAR) e Aplicação de IA na Defesa

## Tecnologias e Frameworks
- **Frameworks:** MITRE ATT&CK, NIST CSF, SOC-MM
- **Logs & SIEM:** Elastic Stack, Wazuh, Splunk
- **Detecção & Automação:** Sigma Rules, Python, APIs de Threat Intel

```
bash

soc-studies-lab/
│
├── README.md                           # Visão geral, mapa de estudos e índice
├── docs/                               # Anotações teóricas e resumos
│   ├── 01-monitoring-and-detection/
│   ├── 02-siem-techniques/
│   ├── 03-soc-management-and-governance/
│   └── 04-ai-and-ueba/
│
├── labs-and-hands-on/                  # Laboratórios e simulações defensivas
│   ├── log-parsing/                    # Parsing de logs de firewall, SO e proxy
│   ├── detection-rules/                # Regras em Sigma, YARA e Snort/Suricata
│   └── automation-playbooks/           # Scripts Python/Ansible/SOAR para triagem
│
└── resources/                          # Cheatsheets, referências e links úteis
```

## Conteúdo Relevante para Cada Módulo

​01. Traffic, Log Monitoring & Detection
​Conceitos: Coleta de eventos (Syslog, Windows Event Logs, NetFlow/IPFIX), arquitetura de agentes de monitoramento (Fluentd, Logstash, Wazuh Agent).
​Atividades Práticas: Mapeamento de fontes de dados vitais para detecção de anomalias na rede e em hosts.

​02. SIEM Tools and Techniques
​Conceitos: Normalização de logs, correlação de eventos em tempo real, retenção e consulta eficiente.
​Atividades Práticas: Criação de consultas de busca (SPL do Splunk, KQL do Elastic) e regras de detecção genéricas convertidas para o padrão Sigma.

​03. SOC Management, Governance & Maturity Models
​Conceitos: Modelos de maturidade (SOC-MM), gestão de incidentes (NIST SP 800-61, ISO 27035), definição de KPIs/SLAs (MTTD, MTTR).
​Atividades Práticas: Modelos de relatórios de incidentes e playbooks de resposta documentados em Markdown.

​04. UEBA, Automation & AI in SOC Operations
​Conceitos: Análise comportamental de usuários e entidades (UEBA), orquestração de resposta (SOAR), aplicação de IA/LLMs na triagem inicial e sumarização de alertas.
​Atividades Práticas: Scripts para enriquecimento automático de alertas (ex: consulta automática de reputação de IP/Hash em APIs de inteligência de ameaças) e automação de rotinas repetitivas do Analista L1.


## Módulo 1 (Traffic, Log Monitoring & Detection)

Para estruturar os scripts em Python do Módulo 1 (Traffic, Log Monitoring & Detection) focando em conceitos modernos de monitoramento e análise de eventos, a abordagem recomendada é trabalhar com análise assíncrona de tráfego (captura e parsing de pacotes) e coleta e estruturação de logs (Windows Event Logs ou arquivos de log de sistema).
