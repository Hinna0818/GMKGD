--建库
CREATE DATABASE gutdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
use gutdb;

-- 建表
CREATE TABLE Microbes (
    Microbe_id VARCHAR(10) PRIMARY KEY,
    GM_name VARCHAR(255) NOT NULL,
    NCBI_ID VARCHAR(50),
    GM_Rank VARCHAR(255),
    Strain VARCHAR(255)
);

CREATE TABLE Metabolites (
    Metabolite_id VARCHAR(10) PRIMARY KEY,
    Metabolite_name VARCHAR(255) NOT NULL,
    PubChem_ID VARCHAR(20),
    ChEBI_ID VARCHAR(20),
    HMDB_ID  VARCHAR(20)
);

CREATE TABLE Targets (
    Gene_id VARCHAR(10) PRIMARY KEY,
    Gene_name VARCHAR(255) NOT NULL,
    Gene_symbol VARCHAR(50),
    NCBI_geneID VARCHAR(50)
);

CREATE TABLE Diseases (
    Disease_id VARCHAR(10) PRIMARY KEY,
    Disease_name VARCHAR(255) NOT NULL,
    DOID VARCHAR(50),
    Description TEXT
);

CREATE TABLE FoodSources (
    Food_id VARCHAR(10) PRIMARY KEY,
    Food_name VARCHAR(255) NOT NULL,
    Category VARCHAR(100),
    Nutrient_content TEXT
);

CREATE TABLE Microbe_Metabolite (
    Microbe_id VARCHAR(10),
    Metabolite_id VARCHAR(10),
    PMID VARCHAR(20),
    PRIMARY KEY (Microbe_id, Metabolite_id, PMID),
    FOREIGN KEY (Microbe_id) REFERENCES Microbes(Microbe_id),
    FOREIGN KEY (Metabolite_id) REFERENCES Metabolites(Metabolite_id)
);

CREATE TABLE Metabolite_Food (
    Metabolite_id VARCHAR(10),
    Food_id VARCHAR(10),
    PRIMARY KEY (Food_id, Metabolite_id),
    FOREIGN KEY (Food_id) REFERENCES FoodSources(Food_id),
    FOREIGN KEY (Metabolite_id) REFERENCES Metabolites(Metabolite_id)
);

CREATE TABLE Metabolite_Target (
    Metabolite_id VARCHAR(10),
    Gene_id VARCHAR(10),
    Alteration VARCHAR(20),
    PMID VARCHAR(20),
    PRIMARY KEY (Metabolite_id, Gene_id, PMID),
    FOREIGN KEY (Metabolite_id) REFERENCES Metabolites(Metabolite_id),
    FOREIGN KEY (Gene_id) REFERENCES Targets(Gene_id)
);


CREATE TABLE Gene_Disease (
    Gene_id VARCHAR(10),
    Disease_id VARCHAR(10),
    PMID VARCHAR(20),
    PRIMARY KEY (Gene_id, Disease_id, PMID),
    FOREIGN KEY (Gene_id) REFERENCES Targets(Gene_id),
    FOREIGN KEY (Disease_id) REFERENCES Diseases(Disease_id)
);