library(tidyverse)
library(cowplot)
library(ggradar)
library(ggstatsplot)
library(ggExtra)

# set standard theme
theme_set(
  theme_minimal_hgrid(10)
)

count_entries_by_country <- function(
  df,
  variable_to_count,
  title = "No title",
  xlabel = "Name of variable",
  ylabel = "Number of 'entries'",
  color_scale = c("#999999", "#E69F00")) {
  
  # plots facet grids to depict counts of a variable
  # across countries
  
  plot <- ggplot(data = df,
                 aes(x = variable_to_count, fill = variable_to_count)) +
    geom_bar(colour = "black") +
    ggtitle(title) +
    scale_fill_manual(values = color_scale) +
    scale_y_continuous(expand = expansion(mult = c(0, 0.1))) +
    facet_wrap( ~ country) +
    labs(x = xlabel,
         y = ylabel) +
    theme(
      plot.title = element_text(lineheight = 1, face = "bold"),
      strip.text.x = element_text(size = 10, face = "bold"),
      strip.background = element_rect(
        color = "black",
        fill = "orange",
        linetype = "solid"
      ),
      legend.position = "none"
    )
  
  return(plot)
}

program_radar <- function(df, uni) {
  
  # plots radar plot of divisions for given university
  
  processed_df <-df[df$uni_name == uni, ] 
  
  df_radar <- processed_df %>%
    group_by(country) %>%
    summarise(
      D1 = mean(`D1`),
      D2 = mean(`D2`),
      D3 = mean(`D3`),
      D4 = mean(`D4`),
      D5 = mean(`D5`),
      D6 = mean(`D6`),
    )
  
  plot <- ggradar(df_radar,
                  values.radar = c(0, 0.5, 1),
                  background.circle.colour = "white",
                  gridline.min.linetype = 1,
                  gridline.mid.linetype = 1,
                  gridline.max.linetype = 1,)
  
  return(plot)
}








