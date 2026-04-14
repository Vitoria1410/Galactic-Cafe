
# 🛸 Galactic Snack Bar - Estação Espacial L0-F1

Este projeto é um simulador de cafeteria espacial desenvolvido em Python com Pygame. O jogador assume o papel de um barista intergaláctico servindo diferentes espécies de alienígenas em uma estação de repouso no espaço.

## 🕹️ Funcionalidades Implementadas

- **Sistema de Fila:** Aliens (Cogumelo, Ciborgue e Tentáculos) entram pela direita, aguardam o pedido no balcão e saem pela esquerda ao serem servidos.
- **Console de Preparo:** Painel inferior com botões coloridos para Nitrogen (Azul), Parafusos (Cinza) e Combustível Estelar (Verde).
- **Feedback Visual:** Partículas de fumaça branca e faíscas coloridas ao preparar as bebidas, com mudança de cor do copo.
- **Efeito Antigravidade:** Todos os personagens e elementos flutuam suavemente usando oscilação senoidal (simulando baixa gravidade).
- **Progressão:** Pontuação acumulada (+100 por pedido correto) e aumento gradativo de velocidade a cada 500 pontos.
- **Telas:** Menu Neon, Jogo principal e Tela de Game Over.

## 📂 Estrutura de Arquivos

- `main.py`: Loop principal, lógica dos clientes, partículas e estados do jogo.
- `settings.py`: Configurações globais, cores (Neon Cyan, Hot Pink, Space Deep) e constantes de gameplay.
- `/assets`: Pasta preparada para receber sprites e sons (o código atual usa desenhos procedurais para garantir execução imediata).

## 🚀 Como Executar

1. Certifique-se de ter o Python e Pygame instalados:
   ```bash
   pip install pygame
   ```
2. Execute o jogo:
   ```bash
   python main.py
   ```

## 🎨 Especificações Técnicas
- **Resolução:** 800x600 pixels.
- **Estética:** Retro/Cyberpunk com paleta Neon.
- **Controles:** Mouse para interagir com o console de preparo.

---
*Desenvolvido com ajuda do Antigravity IA.*
