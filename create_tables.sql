--建库
CREATE DATABASE gutdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
use gutdb;

-- 建表
CREATE TABLE Microbes (
    microbe_id VARCHAR(10) PRIMARY KEY,
    GM_name VARCHAR(255) NOT NULL,
    NCBI_ID VARCHAR(50),
    GM_Rank VARCHAR(255),
    strain VARCHAR(255)
);

CREATE TABLE Metabolites (
    metabolite_id VARCHAR(10) PRIMARY KEY,
    metabolite_name VARCHAR(255) NOT NULL,
    chemical_formula VARCHAR(100),
    smiles TEXT,
    inchi TEXT
);

CREATE TABLE Targets (
    Gene_id VARCHAR(10) PRIMARY KEY,
    Gene_name VARCHAR(255) NOT NULL,
    gene_symbol VARCHAR(50),
    uniprot_id VARCHAR(50)
);

CREATE TABLE Diseases (
    disease_id VARCHAR(10) PRIMARY KEY,
    disease_name VARCHAR(255) NOT NULL,
    doid VARCHAR(50),
    description TEXT
);

CREATE TABLE FoodSources (
    food_id VARCHAR(10) PRIMARY KEY,
    food_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    nutrient_content TEXT
);

CREATE TABLE Microbe_Metabolite (
    microbe_id VARCHAR(10),
    metabolite_id VARCHAR(10),
    PRIMARY KEY (microbe_id, metabolite_id),
    FOREIGN KEY (microbe_id) REFERENCES Microbes(microbe_id),
    FOREIGN KEY (metabolite_id) REFERENCES Metabolites(metabolite_id)
);

CREATE TABLE Metabolite_Food (
    metabolite_id VARCHAR(10),
    food_id VARCHAR(10),
    PRIMARY KEY (food_id, metabolite_id),
    FOREIGN KEY (food_id) REFERENCES FoodSources(food_id),
    FOREIGN KEY (metabolite_id) REFERENCES Metabolites(metabolite_id)
);

CREATE TABLE Metabolite_Target (
    metabolite_id VARCHAR(10),
    Gene_id VARCHAR(10),
    PRIMARY KEY (metabolite_id, Gene_id),
    FOREIGN KEY (metabolite_id) REFERENCES Metabolites(metabolite_id),
    FOREIGN KEY (Gene_id) REFERENCES Targets(Gene_id)
);


CREATE TABLE Metabolite_Disease (
    metabolite_id VARCHAR(10),
    disease_id VARCHAR(10),
    PRIMARY KEY (metabolite_id, disease_id),
    FOREIGN KEY (metabolite_id) REFERENCES Metabolites(Gene_id),
    FOREIGN KEY (disease_id) REFERENCES Diseases(disease_id)
);
