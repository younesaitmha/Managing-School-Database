SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Table `sql2345403`.`Filiere`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sql2345403`.`Filiere` (
  `idFiliere` INT NOT NULL AUTO_INCREMENT,
  `nomFiliere` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`idFiliere`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sql2345403`.`Etudiant`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sql2345403`.`Etudiant` (
  `idEtudiant` INT NOT NULL AUTO_INCREMENT,
  `nom` VARCHAR(50) NOT NULL,
  `prenom` VARCHAR(50) NOT NULL,
  `age` INT NOT NULL,
  `IdFiliereFK` INT NULL,
  PRIMARY KEY (`idEtudiant`),
  CONSTRAINT `IdFiliereFK`
    FOREIGN KEY (`IdFiliereFK`)
    REFERENCES `sql2345403`.`Filiere` (`idFiliere`)
    ON DELETE SET NULL
    ON UPDATE SET NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = DEFAULT;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
