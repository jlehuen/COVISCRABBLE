#!/usr/bin/env python3
#coding:utf-8
"""
render_html.py - Moteur de rendu HTML5 autonome pour OpenSpec Dashboard.
Génère une interface riche, réactive et autonome sans dépendance Jinja.
"""

import os
import json
from openspec_parser import get_openspec_data

def generate_html(base_dir=None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    data = get_openspec_data(base_dir)
    config = data.get('config', {})
    project_name = config.get('name', 'coviscrabble')
    version = config.get('version', '1.0.0')
    description = config.get('description', '')
    settings = config.get('settings', {})
    
    total_req = data.get('total_requirements', 0)
    total_chg = data.get('total_changes', 0)
    comp_tasks = data.get('completed_tasks', 0)
    total_tasks = data.get('total_tasks', 0)
    progress = data.get('global_progress', 0)

    # Specs HTML
    specs_cards = []
    for spec_file in data.get('specs', []):
        for req in spec_file.get('requirements', []):
            points_html = ""
            if req.get('points'):
                pts = "".join(f"<li>{p}</li>" for p in req['points'])
                points_html = f"<ul style='margin: 0.5rem 0 0 1.25rem; font-size: 0.92rem; color: #475569;'>{pts}</ul>"
            
            raw_text = f"{req.get('id', '')} {req.get('raw_name', '')} {req.get('raw_description', '')}"
            card = f"""
            <div class="spec-card spec-search-item" data-text="{raw_text.replace('"', '&quot;')}">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span class="spec-badge">{req.get('id', '')}</span>
                <span style="font-size: 0.8rem; color: #64748b;"><i class="fas fa-file-code"></i> {req.get('spec_file', '')}</span>
              </div>
              <h4 style="font-size: 1.05rem; font-weight: 700; color: #1e293b; margin-bottom: 0.4rem;">{req.get('name', '')}</h4>
              <p style="color: #475569; font-size: 0.92rem; line-height: 1.5;">{req.get('description', '').replace(chr(10), '<br>')}</p>
              {points_html}
            </div>
            """
            specs_cards.append(card)

    specs_section = "".join(specs_cards)

    # Changes HTML
    changes_cards = []
    for chg in data.get('changes', []):
        tasks_items = []
        for group in chg.get('tasks', {}).get('groups', []):
            t_list = []
            for t in group.get('tasks', []):
                checked = 'checked' if t.get('completed') else ''
                text_style = 'color: #334155;' if t.get('completed') else 'color: #94a3b8;'
                t_list.append(f"""
                <li style="list-style: none; display: flex; align-items: flex-start; gap: 0.5rem; margin-bottom: 0.35rem; font-size: 0.9rem;">
                  <input type="checkbox" disabled {checked} style="margin-top: 0.25rem; cursor: not-allowed;">
                  <span style="{text_style}">{t.get('description', '')}</span>
                </li>
                """)
            tasks_items.append(f"""
            <div style="margin-top: 0.75rem;">
              <div style="font-weight: 700; font-size: 0.85rem; color: #475569; text-transform: uppercase; margin-bottom: 0.3rem;">{group.get('name', '')}</div>
              <ul style="padding-left: 0;">{"".join(t_list)}</ul>
            </div>
            """)

        raw_chg_text = f"{chg.get('id', '')} {chg.get('proposal', {}).get('title', '')}"
        chg_card = f"""
        <div class="change-card spec-search-item" data-text="{raw_chg_text.replace('"', '&quot;')}">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
              <span class="change-id">{chg.get('id', '')}</span>
              <strong style="font-size: 1.05rem; color: #1e293b;">{chg.get('proposal', {}).get('title', chg.get('id', ''))}</strong>
            </div>
            <span class="status-badge" style="background: #dcfce7; color: #166534;"><i class="fas fa-check-circle"></i> {chg.get('status', 'Actif')}</span>
          </div>
          <div style="margin: 0.75rem 0;">
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #64748b; margin-bottom: 0.25rem;">
              <span>Avancement</span>
              <strong>{chg.get('completed_tasks', 0)}/{chg.get('total_tasks', 0)} ({chg.get('percentage', 0)}%)</strong>
            </div>
            <div class="progress-bar-container">
              <div class="progress-bar-fill" style="width: {chg.get('percentage', 0)}%;"></div>
            </div>
          </div>
          <div style="font-size: 0.92rem; color: #334155; margin-top: 0.75rem;">
            {"".join(tasks_items)}
          </div>
        </div>
        """
        changes_cards.append(chg_card)

    changes_section = "".join(changes_cards)

    # Settings Rows
    settings_rows = []
    for k, v in settings.items():
        settings_rows.append(f"""
        <tr>
          <td style="padding: 0.75rem; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #475569;">{k}</td>
          <td style="padding: 0.75rem; border-bottom: 1px solid #e2e8f0; color: #1e293b;"><code>{v}</code></td>
        </tr>
        """)
    settings_section = "".join(settings_rows)

    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OpenSpec Dashboard - {project_name}</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {{
      --primary: #1e293b;
      --primary-light: #334155;
      --accent: #2563eb;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #e2e8f0;
      --text: #334155;
      --success: #16a34a;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 2rem 1.5rem;
    }}
    .container {{
      max-width: 1100px;
      margin: 0 auto;
    }}
    .hero {{
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      color: white;
      border-radius: 12px;
      padding: 2rem;
      margin-bottom: 2rem;
      box-shadow: 0 4px 15px rgba(0,0,0,0.1);
      position: relative;
    }}
    .hero h1 {{
      font-size: 1.8rem;
      font-weight: 800;
      letter-spacing: -0.5px;
      margin-bottom: 0.5rem;
    }}
    .hero p {{
      color: #cbd5e1;
      font-size: 1rem;
      max-width: 800px;
    }}
    .hero-tags {{
      display: flex;
      gap: 0.5rem;
      margin-top: 1rem;
    }}
    .tag {{
      background: rgba(255,255,255,0.12);
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 600;
    }}
    .kpis {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-bottom: 2rem;
    }}
    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.25rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .kpi-label {{
      font-size: 0.8rem;
      text-transform: uppercase;
      font-weight: 700;
      color: #64748b;
      margin-bottom: 0.25rem;
    }}
    .kpi-value {{
      font-size: 1.7rem;
      font-weight: 800;
      color: #0f172a;
    }}
    .search-box {{
      width: 100%;
      padding: 0.75rem 1rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      font-size: 0.95rem;
      margin-bottom: 1.5rem;
      background: white;
    }}
    .search-box:focus {{
      outline: none;
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(37,99,235,0.1);
    }}
    .tabs {{
      display: flex;
      gap: 0.5rem;
      margin-bottom: 1.5rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.5rem;
    }}
    .tab-btn {{
      padding: 0.5rem 1rem;
      border-radius: 6px;
      border: 1px solid transparent;
      background: transparent;
      cursor: pointer;
      font-weight: 600;
      font-size: 0.9rem;
      color: #64748b;
    }}
    .tab-btn.active {{
      background: #eff6ff;
      color: var(--accent);
      border-color: #bfdbfe;
    }}
    .tab-content {{
      display: none;
    }}
    .tab-content.active {{
      display: block;
    }}
    .spec-card, .change-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.25rem;
      margin-bottom: 1rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
      transition: transform 0.15s, box-shadow 0.15s;
    }}
    .spec-card:hover, .change-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 12px rgba(0,0,0,0.06);
    }}
    .spec-badge {{
      background: #eff6ff;
      color: var(--accent);
      border: 1px solid #bfdbfe;
      padding: 0.2rem 0.5rem;
      border-radius: 6px;
      font-family: monospace;
      font-weight: 700;
      font-size: 0.8rem;
    }}
    .change-id {{
      background: #f1f5f9;
      color: #334155;
      padding: 0.2rem 0.5rem;
      border-radius: 6px;
      font-family: monospace;
      font-weight: 700;
      font-size: 0.8rem;
    }}
    .status-badge {{
      padding: 0.2rem 0.5rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
    }}
    .progress-bar-container {{
      background: #e2e8f0;
      border-radius: 9999px;
      height: 8px;
      overflow: hidden;
      margin-top: 0.4rem;
    }}
    .progress-bar-fill {{
      background: var(--success);
      height: 100%;
      border-radius: 9999px;
    }}
    code {{
      background: #f1f5f9;
      padding: 0.15rem 0.35rem;
      border-radius: 4px;
      font-size: 0.85em;
      color: #be185d;
      font-family: monospace;
    }}
    pre {{
      background: #0f172a;
      color: #f8fafc;
      padding: 0.8rem;
      border-radius: 6px;
      overflow-x: auto;
      margin: 0.5rem 0;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="hero">
      <h1><i class="fas fa-layer-group"></i> OpenSpec &mdash; {project_name}</h1>
      <p>{description}</p>
      <div class="hero-tags">
        <span class="tag"><i class="fas fa-tag"></i> Version {version}</span>
        <span class="tag"><i class="fas fa-code"></i> SDD / Spec-Driven Development</span>
      </div>
    </div>

    <div class="kpis">
      <div class="kpi-card">
        <div class="kpi-label"><i class="fas fa-list-check"></i> Exigences</div>
        <div class="kpi-value">{total_req}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label"><i class="fas fa-arrows-spin"></i> Cycles Validés</div>
        <div class="kpi-value">{total_chg}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label"><i class="fas fa-tasks"></i> Tâches Réalisées</div>
        <div class="kpi-value">{comp_tasks} / {total_tasks}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label"><i class="fas fa-chart-line"></i> Progression</div>
        <div class="kpi-value">{progress}%</div>
        <div class="progress-bar-container">
          <div class="progress-bar-fill" style="width: {progress}%;"></div>
        </div>
      </div>
    </div>

    <input type="text" id="specSearch" class="search-box" placeholder="Recherche instantanée (ex: REQ-NET, socket, SHA-256, score, plateau)...">

    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab('specs')"><i class="fas fa-book"></i> Spécifications Vivantes ({total_req})</button>
      <button class="tab-btn" onclick="switchTab('changes')"><i class="fas fa-history"></i> Cycles d'Évolution ({total_chg})</button>
      <button class="tab-btn" onclick="switchTab('config')"><i class="fas fa-sliders"></i> Configuration</button>
    </div>

    <div id="tab-specs" class="tab-content active">
      {specs_section}
    </div>

    <div id="tab-changes" class="tab-content">
      {changes_section}
    </div>

    <div id="tab-config" class="tab-content">
      <div class="spec-card">
        <h3 style="margin-bottom: 1rem; color: #1e293b;"><i class="fas fa-cog"></i> Paramètres Système</h3>
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
          <tbody>
            <tr>
              <td style="padding: 0.75rem; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #475569;">Projet</td>
              <td style="padding: 0.75rem; border-bottom: 1px solid #e2e8f0; color: #1e293b;"><code>{project_name}</code></td>
            </tr>
            <tr>
              <td style="padding: 0.75rem; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #475569;">Version</td>
              <td style="padding: 0.75rem; border-bottom: 1px solid #e2e8f0; color: #1e293b;"><code>v{version}</code></td>
            </tr>
            {settings_section}
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <script>
    function switchTab(tabName) {{
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
      
      const targetBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabName));
      if (targetBtn) targetBtn.classList.add('active');
      
      const targetTab = document.getElementById('tab-' + tabName);
      if (targetTab) targetTab.classList.add('active');
    }}

    const searchInput = document.getElementById('specSearch');
    if (searchInput) {{
      searchInput.addEventListener('input', function(e) {{
        const term = e.target.value.toLowerCase().trim();
        document.querySelectorAll('.spec-search-item').forEach(item => {{
          const text = (item.getAttribute('data-text') || '').toLowerCase();
          item.style.display = text.includes(term) ? '' : 'none';
        }});
      }});
    }}
  </script>
</body>
</html>
"""
    return html_content

def build_specs_html(base_dir=None, output_path=None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if output_path is None:
        output_path = os.path.join(base_dir, 'specs.html')
    
    html = generate_html(base_dir)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return output_path

if __name__ == '__main__':
    out = build_specs_html()
    print(f"OpenSpec dashboard generated: {out}")
