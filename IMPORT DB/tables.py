TABLES = {}
TABLES['MAINTABLE'] = (
    " CREATE TABLE OKFN.MAINTABLE (" 
    " ID INT not null auto_increment," 
    " wname VARCHAR(200) NULL,"     
    " wikidataid VARCHAR(200) NULL," 
    " image VARCHAR(200) NULL," 
    " taxinomic_rank VARCHAR(200) NULL,"     
    " scientific_name VARCHAR(200) NULL," 
    " upper_taxon VARCHAR(200) NULL," 
    
    " kingdom VARCHAR(200) NULL," 
    " phylum VARCHAR(200) NULL,"
    " class_c VARCHAR(200) NULL,"
    " order_c VARCHAR(200) NULL,"
    " family VARCHAR(200) NULL,"
    " genus VARCHAR(200) NULL,"
    " species VARCHAR(200) NULL,"
    " subspecies VARCHAR(200) NULL,"
    
    " listing_cites VARCHAR(200) NULL," 
    " citesid VARCHAR(200) NOT NULL UNIQUE,"   
    " PRIMARY KEY (ID)" 
    " ) ENGINE=InnoDB;")

TABLES['COUNTRIES'] = (
    " CREATE TABLE OKFN.COUNTRIES (" 
    " ID INT not null auto_increment,"
    " countryname VARCHAR(200) NULL,"
    " countrycode VARCHAR(200) NULL,"
    " PRIMARY KEY (ID)" 
    " ) ENGINE=InnoDB;")

TABLES['STATUS'] = (
    " CREATE TABLE OKFN.STATUS (" 
    " ID INT not null auto_increment,"
    " status VARCHAR(200) NULL,"
    " statusfr VARCHAR(200) NULL,"    
    " PRIMARY KEY (ID)" 
    " ) ENGINE=InnoDB;")

TABLES['CITES_DISTRIBUTION'] = (
    " CREATE TABLE OKFN.CITES_DISTRIBUTION (" 
    " ID INT not null auto_increment,"
    " wikidataid VARCHAR(200) NULL,"
    " citesid VARCHAR(200) NULL,"
    " countryid INT NULL,"
    " countrystatus VARCHAR(200) NULL,"
    " FOREIGN KEY (countryid) REFERENCES COUNTRIES(ID),"
    " PRIMARY KEY (ID)" 
    " ) ENGINE=InnoDB;")

#TABLES['CITES_LEGISLATION'] = (
#    " CREATE TABLE OKFN.CITES_LEGISLATION ("
#    " ID INT not null auto_increment,"
#    " citesid VARCHAR(200) NULL,"
#    " countryname VARCHAR(200) NULL,"
#    " countrycode VARCHAR(200) NULL,"
#    " countrytype VARCHAR(200) NULL,"
#    " countrytags VARCHAR(200) NULL,"
#    " FOREIGN KEY (citesid) REFERENCES MAINTABLE(citesid),"
#    " PRIMARY KEY (ID)"
#    " ) ENGINE=InnoDB;")