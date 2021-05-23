METRICS = {
  "AV": ["NETWORK", "LOCAL", "ADJACENT_NETWORK", "PHYSICAL"],
  "AC": ["LOW", "HIGH"],
  "PR": ["NONE", "LOW", "HIGH"],
  "UI": ["NONE", "REQUIRED"],
  "SCOPE": ["UNCHANGED", "CHANGED"],
  "CI": ["HIGH", "LOW", "NONE"],
  "II": ["HIGH", "LOW", "NONE"],
  "AI": ["HIGH", "LOW", "NONE"],
};

NAVEGADORES = ["Chrome", "Firefox", "Safari"];

TOTALSTR = "Total";

function COPYRANGE(range)
{
  return range;
}

function exact_match_counter(range, tomatch)
{
  let sum = 0;
  let i;
  for (i = 0; i < range.length; i++) {
    if (range[i] == tomatch)
      sum += 1;
  }
  return sum;
}

function M_OBSERVADO(r_chrome, r_firefox, r_safari, metric_name)
{
  if (!r_chrome || !r_firefox || !r_safari || !metric_name)
    throw new Error("Faltan parametros");
  let ranges = [r_chrome, r_firefox, r_safari]
  let out = [];
  /* mientras esté hardcodeada la cantidad de parametros para rangos de navegadores siempre se dá cols = 3 */
  let cols = 3; // columnas con datos calculados
  const extra_cols = 2; // columnas con labels o totales

  let rows = METRICS[metric_name].length;
  const extra_rows = 2; // idem extra_cols

  let i;
  let j;
  /* escribir labels primero */
  out.push([]);
  for (j = 1; j < cols + extra_cols - 1; j++)
    out[0][j] = NAVEGADORES[j - 1];
  out[0][j] = TOTALSTR;

  for (i = 1; i < rows + extra_rows - 1; i++) {
    out.push([]);
    out[i][0] = METRICS[metric_name][i - 1];
  }
  out.push([]);
  out[i][0] = TOTALSTR;

  for (i = 1; i < rows + extra_rows - 1; i++) {
    for (j = 1; j < cols + extra_cols - 1; j++) {
      out[i][j] = exact_match_counter(ranges[j-1], METRICS[metric_name][i-1]);
    }
  }

  /* ahora calcular totales */
  let sum;
  for (j = 1; j < cols + extra_cols - 1; j++) {
    sum = 0
    for (i = 1; i < rows + extra_rows - 1; i++)
      sum += out[i][j];
    out[i][j] = sum;
  }

  for (i = 1; i < rows + extra_rows; i++) {
    sum = 0
    for (j = 1; j < cols + extra_cols - 1; j++)
      sum += out[i][j];
    out[i][j] = sum;
  }
  return out;
}

function M_ESPERADO(m_o, no_labels)
{
  let i;
  let j;
  let m_e = [[]];
  for (i = no_labels ? 0 : 1; i < m_o.length; i++) {
    m_e.push([]);
    for (j = no_labels? 0 : 1; j < m_o[i].length; j++) {
      m_e[i][j] = m_o[i][m_o[i].length - 1];
      m_e[i][j] *= m_o[m_o.length - 1][j];
      m_e[i][j] /= m_o[m_o.length - 1][m_o[i].length - 1];
    }
  }
  return m_e;
}

function RXCSTAT(m_o, m_e)
{
  let i;
  let j;
  let sum = 0;
  for (i = 0; i < m_e.length; i++) {
    for (j = 0; j < m_e[i].length; j++) {
      let add = (m_o[i][j] - m_e[i][j]) ** 2;
      add /= m_e[i][j];
      sum += add;
    }
  }
  return sum;
}

function FULL_RXCSTAT(r_chrome, r_firefox, r_safari, metric_name)
{
  let out = [];

  let m_o = M_OBSERVADO(r_chrome, r_firefox, r_safari, metric_name);
  let m_e = M_ESPERADO(m_o);
  let m_o_noextras = [];
  let m_e_noextras = [];

  let i;
  let j;
  for (i = 1; i < m_o.length - 1; i++) {
    m_e_noextras.push([]);
    m_o_noextras.push([]);
    for (j = 1; j < m_o[i].length - 1; j++) {
      m_e_noextras[i - 1][j - 1] = m_e[i][j];
      m_o_noextras[i - 1][j - 1] = m_o[i][j];
    }
  }
  rxcstat = RXCSTAT(m_o_noextras, m_e_noextras);
  r = m_o_noextras.length
  c = m_o_noextras[0].length
  df = (r-1) * (c-1)
  out[0] = ["RxC_stat", "r", "c", "X^2 df"];
  out[1] = [rxcstat, r, c, df];
  return out;
}

function PCOMPZ_PHAT(x1, n1, x2, n2)
{
  return (x1+x2)/(n1+n2);
}

function PCOMPZ(x1, n1, x2, n2)
{
  p1_hat = x1/n1;
  p2_hat = x2/n2;
  p_hat = PCOMPZ_PHAT(x1, n1, x2, n2);
  num = (p1_hat - p2_hat);
  denom = (p_hat*(1-p_hat)*((1/n1) + (1/n2))) ** (1/2);
  z = num / denom;
  return z;
}

function MARASCUILLO(m_o, metric_name, metric_val, qchisq)
{
  let ps = [];
  let row;
  let i;
  let p;
  metric_val = metric_val.toUpperCase();
  for (i = 0; m_o[i][0] != metric_val; i++)
    ;
  if (METRICS[metric_name].length < i)
    throw new Error("Revisar el nombre de métrica y/o el valor de métrica ingresado")
  row = i;
  for (i = 1; i < m_o[row].length - 1; i++) {
    p = m_o[row][i] / m_o[m_o.length - 1][i];
    ps.push(p);
  }

  let out = [];
  let diff;
  let stat;
  let ni;
  let nj;
  let signif;

  out.push([metric_val, "|pi - pj|", "crit", "significant?", "max(pi, pj)"])
  for (i = 0; i < ps.length; i++) {
    for (j = i+1; j < ps.length; j++) {
      diff = Math.abs(ps[i] - ps[j]);
      ni = m_o[m_o.length-1][i+1];
      nj = m_o[m_o.length-1][j+1];
      stat = qchisq**(1/2) * ((ps[i]*(1-ps[i])/ni) + (ps[j]*(1-ps[j])/nj))**(1/2);
      signif = diff > stat ? "yes" : "no";
      row = ["|p" + NAVEGADORES[i][0] + " - p" + NAVEGADORES[j][0] + "|", diff, stat, signif, "p" + (ps[i] > ps[j] ? NAVEGADORES[i][0] : NAVEGADORES[j][0])];
      out.push(row);
    }
  }
  return out;
}

function PROP_RXC(m_o)
{
  let m_vals = [];
  let m_ps = [];
  let ret = [];
  let i;
  let p;
  const r = m_o.length;
  const c = m_o[r - 1].length;
  const total = m_o[r - 1][c - 1];

  for (i = 1; i < r; i++)
    m_vals.push(m_o[i][0]);

  for (i = 1; i < r; i++) {
    p = m_o[i][c - 1] / total;
    m_ps.push(p);
  }

  for (i = 0; i < m_ps.length; i++) {
    ret.push([]);
    ret[i].push(m_vals[i]);
    ret[i].push(m_ps[i]);
  }

  return ret;
}
