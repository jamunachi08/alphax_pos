export function money(n: number, symbol = "SAR") {
  return `${symbol} ${n.toFixed(2)}`;
}
