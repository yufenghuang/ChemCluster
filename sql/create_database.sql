/*
    Prepare database for ChemCluster
*/

CREATE DATABASE IF NOT EXISTS testing;

USE testing;

CREATE TABLE IF NOT EXISTS INCAR (
    ID int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Description longtext,
    Text longtext
);

CREATE TABLE IF NOT EXISTS KPOINTS (
    ID int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Description longtext,
    Text longtext
);

CREATE TABLE IF NOT EXISTS Nanoparticles(
    ID int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    natoms int,
    Description varchar(255),
    Elements varchar(255),
    Coordinates longtext
);

CREATE TABLE IF NOT EXISTS Molecules(
    ID int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    natoms int,
    Molecule varchar(255),
    Elements varchar(255),
    ElementList longtext,
    Coordinates longtext,
    Energy varchar(255),
    POSCAR longtext,
    INCAR_ID int,
    KPOINTS_ID int
);

CREATE TABLE IF NOT EXISTS SurfaceSites(
    ID int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    NP_ID int,
    natoms int,
    Rcut double,
    Elements varchar(255),
    ElementList longtext,
    Coordinates longtext
);

CREATE TABLE IF NOT EXISTS Cluster(
    ID int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    SurfaceID int,
    Energy double,
    isConverged BOOL,
    POSCAR longtext,
    INCAR_ID int,
    KPOINTS_ID int
);

CREATE TABLE IF NOT EXISTS ClusterCO(
    ID int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    SurfaceID int,
    Coordinates longtext,
    Energy double,
    isConverged BOOL,
    POSCAR longtext,
    KPOINTS_ID int,
    INCAR_ID int
);