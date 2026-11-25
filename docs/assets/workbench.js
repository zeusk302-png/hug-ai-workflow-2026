const elements = Object.fromEntries([
  'preset', 'load', 'graph', 'kind', 'add', 'runner', 'input', 'second',
  'keyword', 'mode', 'status', 'result', 'node-title', 'in', 'out',
  'export', 'import', 'json-file', 'second-field', 'filter-field', 'mode-field', 'run',
  'input-field', 'deadline-fields', 'deadline-before', 'deadline-after', 'clear-deadline',
].map(id => [id, document.getElementById(id)]));

const definitions = new Map([
  ['input', '입력'],
  ['validateDeadlines', '날짜 확인'],
  ['compareDeadlines', '마감일 비교'],
  ['nasa', 'NASA 사진 검색'],
  ['compare', '두 문서 비교'],
  ['filter', '관심 단어만 남기기'],
  ['hasRows', '결과가 있는가?'],
  ['display', '결과 표시'],
]);
const presets = {
  deadline: { nodes: ['input', 'validateDeadlines', 'compareDeadlines', 'display'], before: '2026-12-10', after: '2026-12-17' },
  nasa: { nodes: ['input', 'nasa', 'hasRows', 'display'], input: 'moon' },
  diff: { nodes: ['input', 'compare', 'hasRows', 'display'], input: '개회 13:00\n휴식 14:30', second: '개회 13:00\n휴식 14:45' },
  list: { nodes: ['input', 'filter', 'hasRows', 'display'], input: '회의 자료\n공개 자료 조사\n모델 비교', keyword: '자료' },
  blank: { nodes: ['input'], input: '' },
};
const moon = {
  title: 'Nearside of the Moon', nasa_id: 'PIA12235',
  credit: 'ISRO/NASA/JPL-Caltech/Brown Univ.', image: 'assets/moon.jpg',
};
const graph = { nodes: [...presets.deadline.nodes], steps: [], selected: 0, running: false };

function usesDates() {
  return graph.nodes.includes('validateDeadlines') || graph.nodes.includes('compareDeadlines');
}

function usesText() {
  return !usesDates() || ['nasa', 'compare', 'filter'].some(kind => graph.nodes.includes(kind));
}

function el(tag, text, css) {
  const result = document.createElement(tag);
  if (text) result.textContent = text;
  if (css) result.className = css;
  return result;
}

function inspect(index) {
  graph.selected = index;
  const step = graph.steps[index];
  elements['node-title'].textContent = definitions.get(graph.nodes[index]);
  elements.in.textContent = step ? JSON.stringify(step.input, null, 2) : '실행 전';
  elements.out.textContent = step ? JSON.stringify(step.output, null, 2) : '실행 전';
  elements.graph.querySelectorAll('.node').forEach((button, i) => {
    button.setAttribute('aria-pressed', String(i === index));
  });
}

function moveNode(from, to) {
  const [node] = graph.nodes.splice(from, 1);
  graph.nodes.splice(to, 0, node);
  resetResult('순서를 바꿨습니다. 다시 실행해보세요.', to);
}

function mutationButton(text, label, handler, disabled) {
  const button = el('button', text);
  button.type = 'button';
  button.setAttribute('aria-label', label);
  button.disabled = graph.running || disabled;
  button.addEventListener('click', handler);
  return button;
}

function renderGraph() {
  const rows = graph.nodes.map((kind, index) => {
    const step = graph.steps[index];
    const node = el('li', '', kind === 'hasRows' ? 'branch' : '');
    const title = definitions.get(kind);
    const button = el('button', '', 'node' + (step ? ' ' + step.state : ''));
    const status = { done: '완료', error: '실패', skipped: '건너뜀', branch: '안내 경로' };
    button.type = 'button';
    button.append(el('strong', title), el('small', step ? status[step.state] : '실행 전'));
    button.addEventListener('click', () => inspect(index));
    node.append(button);

    if (index > 0) {
      const group = el('div', '', 'move');
      group.append(
        mutationButton('위', title + ' 위로', () => moveNode(index, index - 1), index < 2),
        mutationButton('아래', title + ' 아래로', () => moveNode(index, index + 1), index === graph.nodes.length - 1),
        mutationButton('삭제', title + ' 삭제', () => {
          graph.nodes.splice(index, 1);
          resetResult('노드를 지웠습니다. 다시 실행해보세요.', Math.max(0, index - 1));
        }, false),
      );
      node.append(group);
    }
    return node;
  });
  elements.graph.replaceChildren(...rows);
  elements['mode-field'].hidden = !graph.nodes.includes('nasa');
  elements['second-field'].hidden = !graph.nodes.includes('compare');
  elements['filter-field'].hidden = !graph.nodes.includes('filter');
  elements['deadline-fields'].hidden = !usesDates();
  elements['input-field'].hidden = !usesText();
  for (const key of ['run', 'load', 'add', 'import', 'export', 'clear-deadline']) elements[key].disabled = graph.running;
  inspect(graph.selected);
}

function resetResult(message, selection = 0) {
  graph.steps = [];
  graph.selected = selection;
  elements.result.hidden = true;
  elements.status.textContent = message;
  renderGraph();
}

function imageUrl(value) {
  try {
    const url = new URL(value);
    if (url.origin === 'https://images-assets.nasa.gov') return url.href;
  } catch {
    return '';
  }
  return '';
}

async function searchNasa(query, mode) {
  if (!query) throw new Error('검색어를 입력하세요.');
  if (mode === 'sample') return [moon];
  if (mode === 'empty') return [];
  if (mode === 'failure') throw new Error('연결 시간 초과를 재현했습니다.');

  const url = new URL('https://images-api.nasa.gov/search');
  url.search = new URLSearchParams({ q: query.slice(0, 100), media_type: 'image', page_size: '3' });
  const reply = await fetch(url, { signal: AbortSignal.timeout(12000) });
  if (!reply.ok) throw new Error('NASA 응답 상태: ' + reply.status);
  const json = await reply.json();
  if (!Array.isArray(json.collection?.items)) throw new Error('NASA 응답에서 결과 목록을 찾지 못했습니다.');
  return json.collection.items.map(item => {
    const data = item.data?.[0];
    return {
      title: String(data?.title || '제목 없음'),
      nasa_id: String(data?.nasa_id || ''),
      credit: String(data?.secondary_creator || 'NASA Image and Video Library'),
      image: imageUrl(item.links?.find(link => link.rel === 'preview')?.href),
    };
  });
}

function compareLines(before, after) {
  const first = before.split(/\r?\n/);
  const second = after.split(/\r?\n/);
  return Array.from({ length: Math.max(first.length, second.length) }, (_, index) => ({
    line: index + 1, before: first[index] ?? null, after: second[index] ?? null,
  })).filter(row => row.before !== row.after);
}

function validateDeadlines(dates) {
  const fields = [['before', '기존 마감일'], ['after', '변경 마감일']];
  const missing = fields.filter(([key]) => !dates[key]).map(([, label]) => label);
  if (missing.length) throw new Error(missing.join(', ') + '을(를) 입력하세요.');

  for (const [key, label] of fields) {
    const date = new Date(dates[key]);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(dates[key]) || !Number.isFinite(date.valueOf()) || date.toISOString().slice(0, 10) !== dates[key]) {
      throw new Error(label + '을(를) 유효한 날짜로 입력하세요.');
    }
  }
  return { ...dates, valid: true };
}

function deadlineSummary(result) {
  if (result.differenceDays === 0) return '마감일 그대로';
  const action = result.differenceDays > 0 ? '연장' : '앞당겨짐';
  return Math.abs(result.differenceDays) + '일 ' + action;
}

function showResult(data) {
  elements.result.hidden = false;
  elements.result.replaceChildren();
  if (data.message) {
    elements.result.append(el('p', data.message));
    return;
  }
  if (data.deadlineResult) {
    const result = data.deadlineResult;
    const dates = el('dl', '', 'deadline-result');
    for (const [label, value] of [['기존 마감일', result.before], ['변경 마감일', result.after]]) {
      dates.append(el('dt', label), el('dd', value));
    }
    elements.result.append(el('h3', deadlineSummary(result)), dates);
    return;
  }
  if (!data.rows) {
    elements.result.append(el('p', data.text || '입력 값이 비어 있습니다.'));
    return;
  }
  const photo = data.rows[0];
  if (photo?.nasa_id) {
    if (photo.image) {
      const image = el('img');
      image.src = photo.image;
      image.alt = photo.title;
      elements.result.append(image);
    }
    const link = el('a', photo.title);
    link.href = 'https://images.nasa.gov/details/' + encodeURIComponent(photo.nasa_id);
    elements.result.append(link, el('p', photo.credit, 'footnote'));
    return;
  }
  if (!data.rows.length) {
    elements.result.append(el('p', '표시할 결과가 없습니다.'));
    return;
  }
  const list = el('ul');
  for (const row of data.rows.slice(0, 15)) {
    const text = row.line ? row.line + '번째 줄 · ' + (row.before ?? '(없음)') + ' → ' + (row.after ?? '(없음)') : row.text;
    list.append(el('li', text));
  }
  elements.result.append(el('p', '결과 ' + data.rows.length + '건'), list);
}

function receive(kind, data, form) {
  switch (kind) {
    case 'nasa': return { q: data.text, mode: form.mode };
    case 'compare': return { first: data.text, second: form.other };
    case 'filter': return { text: data.text, keyword: form.keyword };
    case 'validateDeadlines': return data.deadlines;
    case 'compareDeadlines': return data.validatedDeadlines ?? null;
    case 'display': return data.deadlineResult ?? data;
    default: return data;
  }
}

async function execute() {
  graph.running = true;
  graph.steps = [];
  elements.result.hidden = true;
  elements.status.textContent = '워크플로 실행 중…';
  renderGraph();
  const form = { text: elements.input.value, other: elements.second.value, keyword: elements.keyword.value.trim(), mode: elements.mode.value };
  let data = usesText() ? { text: form.text } : {};
  if (usesDates()) data.deadlines = { before: elements['deadline-before'].value, after: elements['deadline-after'].value };
  let stopped = '';
  let focus = 0;

  for (const [index, kind] of graph.nodes.entries()) {
    if (stopped) {
      graph.steps.push({ state: 'skipped', input: null, output: { message: '실행 경로에서 건너뜀' } });
      continue;
    }
    const input = receive(kind, data, form);
    focus = index;
    try {
      let output;
      if (kind === 'validateDeadlines') {
        output = validateDeadlines(input);
        data = { ...data, validatedDeadlines: output };
      }
      if (kind === 'compareDeadlines') {
        if (!input) throw new Error('날짜 확인 노드를 비교 앞에 연결하세요.');
        const differenceDays = (Date.parse(input.after) - Date.parse(input.before)) / 86400000;
        output = { before: input.before, after: input.after, changed: differenceDays !== 0, differenceDays };
        data = { ...data, deadlineResult: output };
      }
      if (kind === 'nasa') data = { ...data, rows: await searchNasa(data.text.trim(), form.mode) };
      if (kind === 'compare') data = { ...data, rows: compareLines(data.text, form.other) };
      if (kind === 'filter') {
        if (!form.keyword) throw new Error('찾을 단어를 입력하세요.');
        data = { ...data, rows: data.text.split(/\r?\n/).filter(line => line.toLowerCase().includes(form.keyword.toLowerCase())).map(text => ({ text })) };
      }
      if (kind === 'hasRows') {
        if (!data.rows) throw new Error('먼저 목록을 생성하는 노드를 연결하세요.');
        if (data.rows.length === 0) {
          data = { ...data, message: '결과가 0건입니다. 입력을 바꾸고 다시 실행하세요.' };
          stopped = '0건 안내 경로를 실행했습니다.';
          showResult(data);
        }
      }
      if (kind === 'display') {
        showResult(data);
        output = data.deadlineResult ?? data;
      }
      graph.steps.push({ state: stopped ? 'branch' : 'done', input, output: output ?? data });
    } catch (error) {
      const message = error.name === 'TimeoutError' ? '연결 시간이 초과되었습니다.' : error.message;
      graph.steps.push({ state: 'error', input, output: { error: message } });
      stopped = definitions.get(kind) + ' 단계 실패 · ' + message;
    }
  }

  elements.status.textContent = stopped || '실행 완료 · ' + graph.steps.length + '개 노드';
  graph.selected = focus;
  graph.running = false;
  renderGraph();
}

for (const [key, value] of definitions) {
  if (key === 'input') continue;
  const option = el('option', value);
  option.value = key;
  elements.kind.append(option);
}

elements.load.addEventListener('click', () => {
  const preset = presets[elements.preset.value];
  graph.nodes = [...preset.nodes];
  elements.input.value = preset.input || '';
  elements.second.value = preset.second || '';
  elements.keyword.value = preset.keyword || '';
  elements.mode.value = 'sample';
  elements['deadline-before'].value = preset.before || '';
  elements['deadline-after'].value = preset.after || '';
  resetResult('예제를 열었습니다.');
});
elements.add.addEventListener('click', () => {
  if (graph.nodes.length >= 12) {
    elements.status.textContent = '실습실에서는 노드를 12개까지 연결할 수 있습니다.';
    return;
  }
  graph.nodes.push(elements.kind.value);
  resetResult('노드를 추가했습니다.', graph.nodes.length - 1);
});
elements['clear-deadline'].addEventListener('click', () => {
  elements['deadline-after'].value = '';
  elements['deadline-after'].focus();
});
elements.runner.addEventListener('submit', event => {
  event.preventDefault();
  if (!graph.running) void execute();
});
elements.export.addEventListener('click', () => {
  const json = JSON.stringify({ version: 1, nodes: graph.nodes }, null, 2);
  const url = URL.createObjectURL(new Blob([json], { type: 'application/json' }));
  const link = el('a');
  link.href = url;
  link.download = 'hug-workflow.json';
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
elements.import.addEventListener('click', () => elements['json-file'].click());
elements['json-file'].addEventListener('change', async () => {
  const file = elements['json-file'].files[0];
  elements['json-file'].value = '';
  if (!file) return;
  try {
    if (file.size > 32768) throw new Error();
    const json = JSON.parse(await file.text());
    const nodes = json?.nodes;
    if (json?.version !== 1 || !Array.isArray(nodes) || nodes[0] !== 'input' ||
        nodes.length > 12 || nodes.slice(1).some(node => node === 'input' || !definitions.has(node))) throw new Error();
    if (graph.running) return;
    graph.nodes = nodes;
    resetResult('워크플로를 불러왔습니다. 새 입력을 넣고 실행하세요.');
  } catch {
    elements.status.textContent = '이 실습실에서 저장한 워크플로 JSON을 선택하세요.';
  }
});
renderGraph();
