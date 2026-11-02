"""
openspec_parser.py - Moteur d'analyse dynamique des spécifications et cycles OpenSpec.
Générique et réutilisable pour tout projet de développement.

Extrait à chaud les métadonnées de config.yaml, les exigences vivantes (specs/*.md)
et l'avancement des changements (changes/*/proposal.md, tasks.md) sans aucune dépendance externe.
"""

import os
import re
import html

def markdown_to_html(text):
    """
    Convertit la syntaxe markdown essentielle en HTML (inline code, blocs de code, gras, liens).
    Échappe d'abord le HTML brut pour garantir la sécurité et préserver les expressions comme <int:id>.
    """
    if not text:
        return ''
    
    # 1. Échapper le HTML d'abord
    escaped = html.escape(text)

    # 2. Blocs de code (triple backticks)
    def repl_pre(m):
        code_content = m.group(1).strip()
        return f'<pre><code>{code_content}</code></pre>'
    escaped = re.sub(r'```(?:\w+)?\r?\n?(.*?)\r?\n?```', repl_pre, escaped, flags=re.DOTALL)

    # 3. Code inline (simple backtick `...`)
    escaped = re.sub(r'`([^`]+)`', r'<code>\1</code>', escaped)

    # 4. Gras (**...**)
    escaped = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', escaped)

    # 5. Liens markdown [texte](url)
    escaped = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', escaped)

    return escaped

def parse_yaml_simple(content):
    """Parseur YAML minimaliste pour config.yaml."""
    data = {}
    current_section = None
    for line in content.splitlines():
        raw = line.strip()
        if not raw or raw.startswith('#'):
            continue
        if line.startswith('  ') and current_section:
            parts = raw.split(':', 1)
            if len(parts) == 2:
                k, v = parts[0].strip(), parts[1].strip().strip('\"\'')
                if current_section not in data:
                    data[current_section] = {}
                data[current_section][k] = v
        else:
            parts = raw.split(':', 1)
            k = parts[0].strip()
            v = parts[1].strip().strip('\"\'') if len(parts) > 1 else ''
            if v:
                data[k] = v
                current_section = None
            else:
                current_section = k
                if current_section not in data:
                    data[current_section] = {}
    return data

def get_openspec_data(base_dir=None):
    """
    Analyse l'ensemble du dossier openspec/ et retourne une structure complète
    pour le tableau de bord HTML5.
    """
    if base_dir is None:
        try:
            from core.config import BASE_DIR
            base_dir = BASE_DIR
        except ImportError:
            base_dir = os.getcwd()

    openspec_dir = os.path.join(base_dir, 'openspec')
    if not os.path.exists(openspec_dir):
        return None

    # 1. Configuration du projet
    config = {
        'name': os.path.basename(base_dir),
        'description': '',
        'version': '1.0.0',
        'schema': 'openspec/v1',
        'settings': {}
    }
    config_path = os.path.join(openspec_dir, 'config.yaml')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                raw_cfg = parse_yaml_simple(f.read())
            if 'project' in raw_cfg and isinstance(raw_cfg['project'], dict):
                config['name'] = raw_cfg['project'].get('name', config['name'])
                config['description'] = raw_cfg['project'].get('description', '')
                config['version'] = raw_cfg['project'].get('version', '1.0.0')
            if 'settings' in raw_cfg and isinstance(raw_cfg['settings'], dict):
                config['settings'] = raw_cfg['settings']
            if 'schema' in raw_cfg and isinstance(raw_cfg['schema'], str):
                config['schema'] = raw_cfg['schema']
        except Exception:
            pass

    # 2. Spécifications vivantes (specs/*.md)
    specs_dir = os.path.join(openspec_dir, 'specs')
    specs = []
    all_requirements = []
    if os.path.exists(specs_dir):
        for filename in sorted(os.listdir(specs_dir)):
            if filename.endswith('.md'):
                filepath = os.path.join(specs_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception:
                    continue

                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                spec_title = title_match.group(1).strip() if title_match else filename

                req_pattern = re.compile(r'^###\s+(REQ-[\w-]+)\s*:\s*(.+)$', re.MULTILINE)
                matches = list(req_pattern.finditer(content))
                reqs = []
                for i, match in enumerate(matches):
                    req_id = match.group(1).strip()
                    req_name = match.group(2).strip()
                    start_idx = match.end()
                    end_idx = matches[i+1].start() if i + 1 < len(matches) else len(content)
                    body = content[start_idx:end_idx].strip()

                    # Points clés
                    raw_points = [p.strip() for p in re.findall(r'^[*-]\s+(.+)$', body, re.MULTILINE)]
                    points = [markdown_to_html(p) for p in raw_points]
                    req_item = {
                        'id': req_id,
                        'name': markdown_to_html(req_name),
                        'raw_name': req_name,
                        'description': markdown_to_html(body),
                        'raw_description': body,
                        'points': points,
                        'raw_points': raw_points,
                        'spec_file': filename,
                        'status': 'Validé'
                    }
                    reqs.append(req_item)
                    all_requirements.append(req_item)

                specs.append({
                    'filename': filename,
                    'title': spec_title,
                    'requirements': reqs,
                    'count': len(reqs)
                })

    # 3. Cycles de changements (changes/*/)
    changes_dir = os.path.join(openspec_dir, 'changes')
    changes = []
    total_tasks = 0
    completed_tasks = 0

    if os.path.exists(changes_dir):
        for entry in sorted(os.listdir(changes_dir)):
            change_path = os.path.join(changes_dir, entry)
            if not os.path.isdir(change_path):
                continue

            # Proposition
            prop_path = os.path.join(change_path, 'proposal.md')
            proposal_data = {
                'title': entry,
                'why': '',
                'what': '',
                'impact': '',
                'sections': []
            }
            if os.path.exists(prop_path):
                try:
                    with open(prop_path, 'r', encoding='utf-8') as f:
                        pcontent = f.read()
                    ptitle = re.search(r'^#\s+(.+)$', pcontent, re.MULTILINE)
                    if ptitle:
                        proposal_data['title'] = ptitle.group(1).strip()

                    sec_matches = list(re.finditer(r'^##\s+(.+)$', pcontent, re.MULTILINE))
                    for j, sm in enumerate(sec_matches):
                        sec_title = sm.group(1).strip()
                        s_start = sm.end()
                        s_end = sec_matches[j+1].start() if j + 1 < len(sec_matches) else len(pcontent)
                        sec_body = pcontent[s_start:s_end].strip()
                        formatted_sec_body = markdown_to_html(sec_body)
                        proposal_data['sections'].append({
                            'title': sec_title,
                            'content': formatted_sec_body,
                            'raw_content': sec_body
                        })
                        st_lower = sec_title.lower()
                        if 'contexte' in st_lower or 'why' in st_lower or 'pourquoi' in st_lower:
                            proposal_data['why'] = formatted_sec_body
                        elif 'proposition' in st_lower or 'what' in st_lower or 'quoi' in st_lower:
                            proposal_data['what'] = formatted_sec_body
                        elif 'impact' in st_lower:
                            proposal_data['impact'] = formatted_sec_body
                except Exception:
                    pass

            # Tâches (tasks.md)
            tasks_path = os.path.join(change_path, 'tasks.md')
            task_groups = []
            c_total = 0
            c_completed = 0
            if os.path.exists(tasks_path):
                try:
                    with open(tasks_path, 'r', encoding='utf-8') as f:
                        tcontent = f.read()

                    current_group = {'name': 'Tâches principales', 'tasks': []}
                    for tline in tcontent.splitlines():
                        tline_strip = tline.strip()
                        if tline_strip.startswith('## '):
                            if current_group['tasks']:
                                task_groups.append(current_group)
                            current_group = {'name': tline_strip[3:].strip(), 'tasks': []}
                        elif re.match(r'^[*-]\s*\[[ xX]\]', tline_strip):
                            is_done = bool(re.match(r'^[*-]\s*\[[xX]\]', tline_strip))
                            task_desc = re.sub(r'^[*-]\s*\[[ xX]\]\s*', '', tline_strip).strip()
                            is_subtask = tline.startswith('  ') or tline.startswith('\t')
                            c_total += 1
                            if is_done:
                                c_completed += 1
                            current_group['tasks'].append({
                                'description': markdown_to_html(task_desc),
                                'raw_description': task_desc,
                                'completed': is_done,
                                'is_subtask': is_subtask
                            })
                    if current_group['tasks']:
                        task_groups.append(current_group)
                except Exception:
                    pass

            total_tasks += c_total
            completed_tasks += c_completed
            c_pct = int((c_completed / c_total) * 100) if c_total > 0 else 100

            changes.append({
                'id': entry,
                'proposal': proposal_data,
                'task_groups': task_groups,
                'total_tasks': c_total,
                'completed_tasks': c_completed,
                'percentage': c_pct,
                'status': 'Terminé' if c_pct == 100 else 'En cours'
            })

    global_pct = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 100

    return {
        'config': config,
        'specs': specs,
        'all_requirements': all_requirements,
        'total_requirements': len(all_requirements),
        'changes': changes,
        'total_changes': len(changes),
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'global_progress': global_pct
    }
