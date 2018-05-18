#draw the species tree
#shimw
#2018/5/18
library(ggtree)
library("treeio")
nwk_file=system.file("extdata","/opt/shimw/github/tax_list.nwk",package = "treeio")
tree <- read.tree("/opt/shimw/github/tax_list.nwk")
ggtree(tree, color="firebrick", size=0.8, linetype="dotdash",layout = "circular")+geom_tippoint(color="black", size=2.5)+
  geom_nodepoint(color="firebrick",size=1.5)+geom_tiplab2(hjust = -0.1)+xlim(0,1200)
ggsave(
  filename = "tree.png",
  plot = p,
  device = "png",
  width = 9,
  height = 9,
  path = "/opt/shimw/"
)
