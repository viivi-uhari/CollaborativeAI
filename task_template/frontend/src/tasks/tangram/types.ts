export type Point = {
  x: number
  y: number
} // Represents a point as a tuple of x, y coordinates

export type TangramPiece = {
  id: string // Name of the piece
  points: Point[] // Array of points defining the piece
}

export type TangramGame = {
  st_1?: TangramPiece
  st_2?: TangramPiece
  mt_1?: TangramPiece
  lt_1?: TangramPiece
  lt_2?: TangramPiece
  pg_1?: TangramPiece
  sq_1?: TangramPiece
}
