# Este código baixa as votações da câmara e faz as transformações pertinentes
# Para exemplificar, foi utilizado o ano de 2026 (o processo é o mesmo para qualquer ano)

# Pacotes
install.packages("httr")
install.packages("readr")
install.packages("tidyverse")
install.packages("writexl")

library(httr)
library(readr)
library(tidyverse)
library(writexl)

# Baixando os dados
url_votacoes2026 <- "http://dadosabertos.camara.leg.br/arquivos/votacoes/csv/votacoes-2026.csv"
Votacoes_2026 <- read.csv2(url_votacoes2026)

# Mantendo apenas votações de plenário não unânimes
Votacoes_plenario2026 <- Votacoes_2026 %>% 
  select(id, data, dataHoraRegistro, siglaOrgao, aprovacao, votosSim, votosNao, votosOutros, descricao, ultimaAberturaVotacao_descricao) %>%
  filter(siglaOrgao == "PLEN", !(votosNao == 0), !is.na(aprovacao)) %>% 
  select(-siglaOrgao)

# Baixando as orientações de bancada
url_orientacoes_bancada2026 <- "http://dadosabertos.camara.leg.br/arquivos/votacoesOrientacoes/csv/votacoesOrientacoes-2026.csv"
orientacoes_bancada2026 <- read.csv2(url_orientacoes_bancada2026)

# Agregando as orientações e unindo ao dataframe principal
orientacoes_agregado2026 <- orientacoes_bancada2026 %>%
  filter(orientacao %in% c("Sim", "Não")) %>%
  group_by(idVotacao, orientacao) %>%
  summarise(bancadas = paste(siglaBancada, collapse = ", "), .groups = 'drop') %>%
  pivot_wider(
    names_from = orientacao, 
    values_from = bancadas, 
    names_prefix = "orientaram_"
  )

Votacoes_plenario2026 <- Votacoes_plenario2026 %>%
  left_join(orientacoes_agregado2026, by = c("id" = "idVotacao"))

# Baixando as proposições afetadas e unindo ao dataframe principal
url_proposicoes_afetadas2026 <- "http://dadosabertos.camara.leg.br/arquivos/votacoesProposicoes/csv/votacoesProposicoes-2026.csv"
proposicoes_afetadas2026 <- read.csv2(url_proposicoes_afetadas2026)

Votacoes_plenario2026 <- Votacoes_plenario2026 %>%
  left_join(
    select(proposicoes_afetadas2026, idVotacao, proposicao_titulo, proposicao_ementa),
    by = c("id" = "idVotacao")
  )

# Exportando para xlsx para realizar a classificação manual
write_xlsx(Votacoes_plenario2026, "votacoes_plenario_2026.xlsx")