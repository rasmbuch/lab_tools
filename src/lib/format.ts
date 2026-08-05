const SUPERSCRIPTS: Record<string, string> = {
  '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
  '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
  '-': '⁻',
};

function toSuperscript(exp: string): string {
  return exp.replace(/[0-9-]/g, (ch) => SUPERSCRIPTS[ch]);
}

function formatSci(value: number, n: number): string {
  const [coeff, exp] = value.toExponential(n - 1).split('e');
  const cleanCoeff = coeff.includes('.') ? coeff.replace(/\.?0+$/, '') : coeff;
  const cleanExp = exp.replace('+', '');
  return `${cleanCoeff} × 10${toSuperscript(cleanExp)}`;
}

export function sigfigs(value: number, n: number = 4): string {
  if (!Number.isFinite(value) || value === 0) return '0';
  const abs = Math.abs(value);
  if (abs >= 0.001 && abs < 1e6) {
    const s = value.toPrecision(n);
    if (s.includes('e')) return formatSci(value, n);
    if (s.includes('.')) return s.replace(/\.?0+$/, '');
    return s;
  }
  return formatSci(value, n);
}
