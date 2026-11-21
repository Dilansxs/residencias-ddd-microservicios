from dataclasses import dataclass


@dataclass(frozen=True)
class IdentificadorResidencia:
    valor: str

    def __post_init__(self) -> None:
        if not self.valor or not self.valor.strip():
            raise ValueError("El identificador de residencia no puede estar vacío.")


@dataclass(frozen=True)
class ReferenciaResidente:
    codigo: str

    def __post_init__(self) -> None:
        if not self.codigo or not self.codigo.strip():
            raise ValueError("La referencia del residente no puede estar vacía.")


@dataclass(frozen=True)
class Medicion:
    valor: float
    unidad: str


@dataclass(frozen=True)
class Limite:
    minimo: float
    maximo: float
    severidad: str

    def es_superado_por(self, valor: float) -> bool:
        return valor < self.minimo or valor > self.maximo