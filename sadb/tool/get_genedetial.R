library('biomaRt')
library('dplyr')
Args <- commandArgs()
taxon_id <- Args[6]
taxon_list <- readr::read_csv('/home/zhangna/SAdatabase/result/ensembl/Species_whole.csv')
science_name=taxon_list$`Scientific name`[which(taxon_list$`Taxon ID`==taxon_id)]
select_dataset=paste(tolower(substring(strsplit(science_name," ")[[1]][1],1,1)),
                     strsplit(science_name," ")[[1]][2],"_gene_ensembl",sep = "")


ensembl=useMart(host='asia.ensembl.org', 
                  biomart='ENSEMBL_MART_ENSEMBL', 
                  dataset=select_dataset)
Attributes=c('ensembl_gene_id',
             'start_position',
             'end_position',
             'external_gene_name',
             'description',
             'gene_biotype',
             'chromosome_name',
             'entrezgene',
             'hgnc_id')
Transcript =c('ensembl_gene_id',
              'ensembl_transcript_id',
              'start_position',
              'end_position',
              'transcript_length',
              'ensembl_peptide_id',
              'transcript_start',
              'transcript_end',
              'cds_length',
              'uniprotsptrembl',
              'transcript_biotype')
exon = c('ensembl_transcript_id',
         'ensembl_exon_id',
         'exon_chrom_start',
         'exon_chrom_end')

Protein=c('ensembl_gene_id',
          'ensembl_peptide_id',
          'pfam',
          'pfam_start',
          'pfam_end')
go_term=c('ensembl_gene_id',
          'go_id',
          'name_1006',
          'go_linkage_type',
          'namespace_1003')
phenotype=c('ensembl_gene_id',
            'phenotype_description',
            'study_external_id',
            'source_name')

pathway=c('ensembl_gene_id','kegg_enzyme')

paralogue=c('ensembl_gene_id',paste(tolower(substring(strsplit(science_name," ")[[1]][1],1,1)),
                                    strsplit(science_name," ")[[1]][2],"_paralog_ensembl_gene",sep = ""))



gene_detail=getBM(attributes=Attributes,mart = ensembl)
print("detail")
gene_structures=getBM(attributes=Transcript,mart = ensembl)
print("structures")
Transcript_exon=getBM(attributes=exon,mart = ensembl)
print("exon")
gene_Protein=getBM(attributes=Protein,mart = ensembl)
print("Protein")
go_term=getBM(attributes=go_term,mart = ensembl)
go_term=dplyr::filter(go_term,go_id!="")
print("go_term")
gene_phenotype=tryCatch(getBM(attributes=phenotype,mart = ensembl),error=function(e){return(FALSE)})
print("phenotype")
gene_pathway=tryCatch(getBM(attributes=pathway,mart = ensembl),error=function(e){return(FALSE)})
print("pathway")
gene_paralogue=getBM(attributes=paralogue,mart = ensembl)
print("paralogue")
names(gene_paralogue)[2]="paralog_ensembl_gene"


readr::write_csv(gene_detail,"/opt/shimw/gene_detail.csv")
readr::write_csv(gene_structures,"/opt/shimw/gene_structures.csv")
readr::write_csv(Transcript_exon,"/opt/shimw/Transcript_exon.csv")
readr::write_csv(gene_Protein,"/opt/shimw/gene_Protein.csv")
readr::write_csv(go_term,"/opt/shimw/go_term.csv")
if (gene_phenotype!=F){readr::write_csv(gene_phenotype,"/opt/shimw/gene_phenotype.csv")}
if (gene_pathway!=F){readr::write_csv(gene_pathway,"/opt/shimw/gene_pathway.csv")}

readr::write_csv(gene_paralogue,"/opt/shimw/gene_paralogue.csv")

list_attr=listAttributes(ensembl)

purrr::map(grep(pattern = "_homolog_ensembl_gene", x = list_attr$name, value = TRUE),function(x){
  specie=strsplit(x,split = "_")[[1]][1]
  homolog=c('ensembl_gene_id',
            'external_gene_name',
            paste(specie,"homolog_ensembl_gene",sep = "_"),
            paste(specie,"homolog_associated_gene_name",sep = "_"),
            paste(specie,"homolog_perc_id",sep = "_"),
            paste(specie,"homolog_perc_id_r1",sep = "_"),
            paste(specie,"homolog_wga_coverage",sep = "_"),
            paste(specie,"homolog_orthology_confidence",sep = "_"))
  gene_homolog=getBM(attributes=homolog,mart = ensembl)
  names(gene_homolog)=c("ensembl_gene_id",
                            "external_gene_name",
                            "ortholog",
                            "ortholog_external_gene_name",
                            "homolog_perc_id",
                            "homolog_perc_id_r1",
                            "homolog_wga_coverage",
                            "homolog_orthology_confidence")
  
  gene_homolog=dplyr::filter(gene_homolog,ortholog!="")
  
  return(gene_homolog)
})%>%
  dplyr::bind_rows()->gene_homolog
print("homolog")
readr::write_csv(gene_homolog,"/opt/shimw/gene_homolog.csv")



