CREATE TABLE Producto (
    fabricante varchar(50),
    modelo varchar(50),
    tipo varchar(50),
    PRIMARY KEY (modelo)
);

CREATE TABLE PC (
    modelo varchar(50),
    velocidad float,
    ram int,
    disco int,
    precio float,
    PRIMARY KEY (modelo),
    FOREIGN KEY (modelo) REFERENCES Producto(modelo) ON DELETE CASCADE
);
