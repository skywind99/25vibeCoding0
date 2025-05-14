import streamlit as st

# HTML 내용을 문자열로 준비합니다.
# 실제 사용 시에는 전체 HTML 코드를 이 안에 넣어야 합니다.
# 편의상 파일에서 읽어올 수도 있습니다.
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>주기율표 시뮬레이터</title>
  <style>
    body {
      margin: 0;
      background: #1e1e1e; /* Streamlit 배경과 다를 수 있으므로 iframe 내에서만 적용됨 */
      color: white;
      font-family: 'Arial', sans-serif;
      display: flex;
      min-height: 100vh; /* iframe 높이에 맞춰 조정될 수 있음 */
    }
    .left-panel {
      flex: 4;
      display: flex;
      flex-direction: column;
      padding: 10px;
    }
    .right-panel {
      flex: 2;
      padding: 10px;
      border-left: 2px solid #444;
      display: flex;
      flex-direction: column;
    }
    h1 {
      text-align: center;
      margin: 10px 0;
    }
    .canvas {
      height: 300px; /* 고정 높이 */
      background: #111;
      border: 2px solid #444;
      position: relative;
      margin-bottom: 10px;
      overflow: hidden;
    }
    .formula-box {
      height: 50px;
      background: #222;
      border: 2px solid #444;
      padding: 8px;
      font-size: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 10px;
    }
    .recommendations {
      background: #222;
      border: 2px solid #444;
      padding: 8px;
      font-size: 14px;
      flex-grow: 1; /* left-panel 내에서 유효 */
      overflow-y: auto;
      margin-bottom: 10px;
      min-height: 150px; /* 추천 영역 최소 높이 확보 */
    }
    .buttons {
      display: flex;
      gap: 10px;
      margin-bottom: 10px;
    }
    .btn {
      flex: 1;
      padding: 8px;
      background: #333;
      color: white;
      border: 1px solid #555;
      border-radius: 4px;
      cursor: pointer;
    }
    .btn:hover {
      background: #444;
    }
    .periodic-container {
      overflow-y: auto;
      /* max-height는 iframe 높이에 따라 달라지므로 주의 */
      /* calc(100vh - 50px)는 iframe 내에서는 다르게 동작할 수 있음 */
      max-height: 500px; /* 예시 고정 높이, iframe 높이 고려 필요 */
    }
    .table-wrapper {
      display: grid;
      grid-template-columns: repeat(18, 36px);
      grid-auto-rows: 36px;
      gap: 3px;
      justify-content: center;
      padding: 10px;
    }
    .element {
      border-radius: 4px;
      text-align: center;
      font-size: 12px;
      padding: 2px;
      cursor: grab;
      user-select: none;
      color: white;
      display: flex;
      flex-direction: column;
      justify-content: center;
      position: relative;
    }
    .element:hover {
      transform: scale(1.1);
      z-index: 10;
    }
    .element span {
      display: block;
      font-size: 7px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .element .atomic-number {
      position: absolute;
      top: 1px;
      left: 2px;
      font-size: 6px;
    }
    .empty {
      background: transparent;
      border: none;
      cursor: default;
    }
    .atom {
      position: absolute;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      cursor: grab;
      user-select: none;
      z-index: 10;
    }
    .bond {
      position: absolute;
      height: 2px;
      background-color: rgba(255, 255, 255, 0.6);
      transform-origin: left center;
      z-index: 5;
    }
    .bond-label {
      position: absolute;
      background-color: rgba(0, 0, 0, 0.7);
      color: white;
      padding: 2px 4px;
      border-radius: 3px;
      font-size: 10px;
      z-index: 6;
    }
    .recommendation-item {
      margin: 5px 0;
      padding: 5px;
      border-radius: 3px;
      cursor: pointer;
    }
    .recommendation-item:hover {
      background: #333;
    }
  </style>
</head>
<body>
  <div class="left-panel">
    <h1>화학식 시뮬레이터</h1>
    <div class="canvas" id="canvas"></div>
    <div class="formula-box" id="formulaBox">화학식을 여기에 보여줍니다</div>
    <div class="recommendations" id="recommendationsBox">
      <h3>화합물 추천</h3>
      <div id="recommendations"></div>
    </div>
    <div class="buttons">
      <button class="btn" id="saveBtn">저장</button>
      <button class="btn" id="resetBtn">초기화</button>
    </div>
  </div>
  <div class="right-panel">
    <div class="periodic-container">
      <div class="table-wrapper" id="periodicTable"></div>
    </div>
  </div>

  <script>
    const table = document.getElementById('periodicTable');
    const canvas = document.getElementById('canvas');
    const formulaBox = document.getElementById('formulaBox');
    const recommendationsBox = document.getElementById('recommendations');
    const saveBtn = document.getElementById('saveBtn');
    const resetBtn = document.getElementById('resetBtn');

    const periodColors = {
      1: "#ff9ff3", 2: "#feca57", 3: "#ff6b6b", 4: "#1dd1a1",
      5: "#54a0ff", 6: "#5f27cd", 7: "#576574"
    };

    const elementsData = {
      1: ['H', '수소', 1, 1], 2: ['He', '헬륨', 18, 1], 3: ['Li', '리튬', 1, 2],
      4: ['Be', '베릴륨', 2, 2], 5: ['B', '붕소', 13, 2], 6: ['C', '탄소', 14, 2],
      7: ['N', '질소', 15, 2], 8: ['O', '산소', 16, 2], 9: ['F', '플루오린', 17, 2],
      10: ['Ne', '네온', 18, 2], 11: ['Na', '나트륨', 1, 3], 12: ['Mg', '마그네슘', 2, 3],
      13: ['Al', '알루미늄', 13, 3], 14: ['Si', '규소', 14, 3], 15: ['P', '인', 15, 3],
      16: ['S', '황', 16, 3], 17: ['Cl', '염소', 17, 3], 18: ['Ar', '아르곤', 18, 3],
      19: ['K', '칼륨', 1, 4], 20: ['Ca', '칼슘', 2, 4], 21: ['Sc', '스칸듐', 3, 4],
      22: ['Ti', '티타늄', 4, 4], 23: ['V', '바나듐', 5, 4], 24: ['Cr', '크롬', 6, 4],
      25: ['Mn', '망간', 7, 4], 26: ['Fe', '철', 8, 4], 27: ['Co', '코발트', 9, 4],
      28: ['Ni', '니켈', 10, 4], 29: ['Cu', '구리', 11, 4], 30: ['Zn', '아연', 12, 4],
      31: ['Ga', '갈륨', 13, 4], 32: ['Ge', '저마늄', 14, 4], 33: ['As', '비소', 15, 4],
      34: ['Se', '셀레늄', 16, 4], 35: ['Br', '브로민', 17, 4], 36: ['Kr', '크립톤', 18, 4]
    };

    const commonCompounds = {
      'H2O': { name: '물', elements: { 'H': 2, 'O': 1 } },
      'NaCl': { name: '소금 (염화나트륨)', elements: { 'Na': 1, 'Cl': 1 } },
      'CO2': { name: '이산화탄소', elements: { 'C': 1, 'O': 2 } },
      'H2': { name: '수소 분자', elements: { 'H': 2 } }, 'O2': { name: '산소 분자', elements: { 'O': 2 } },
      'NH3': { name: '암모니아', elements: { 'N': 1, 'H': 3 } }, 'CH4': { name: '메탄', elements: { 'C': 1, 'H': 4 } },
      'H2SO4': { name: '황산', elements: { 'H': 2, 'S': 1, 'O': 4 } }, 'HCl': { name: '염산', elements: { 'H': 1, 'Cl': 1 } },
      'NaOH': { name: '수산화나트륨', elements: { 'Na': 1, 'O': 1, 'H': 1 } },
      'CaCO3': { name: '탄산칼슘', elements: { 'Ca': 1, 'C': 1, 'O': 3 } },
      'Fe2O3': { name: '산화철', elements: { 'Fe': 2, 'O': 3 } },
      'C6H12O6': { name: '포도당', elements: { 'C': 6, 'H': 12, 'O': 6 } },
      'N2': { name: '질소 분자', elements: { 'N': 2 } }
    };

    const elementCompounds = {};
    Object.keys(commonCompounds).forEach(formula => {
      const compound = commonCompounds[formula];
      Object.keys(compound.elements).forEach(element => {
        if (!elementCompounds[element]) elementCompounds[element] = [];
        if (!elementCompounds[element].includes(formula)) elementCompounds[element].push(formula);
      });
    });

    let symbolCount = {};
    let canvasAtoms = [];
    let bonds = [];
    let nextId = 1;

    for (let period = 1; period <= 7; period++) {
      for (let group = 1; group <= 18; group++) {
        const cell = document.createElement('div');
        const atomicNumber = Object.keys(elementsData).find(key => elementsData[key][3] === period && elementsData[key][2] === group);
        if (atomicNumber && atomicNumber <= 36) {
          const [symbol, name, _group, _period] = elementsData[atomicNumber];
          cell.className = 'element';
          cell.innerHTML = `<div class="atomic-number"><span class="math-inline">\{atomicNumber\}</div\></span>{symbol}<span>${name}</span>`;
          cell.style.backgroundColor = periodColors[_period];
          cell.dataset.symbol = symbol;
          cell.dataset.atomicNumber = atomicNumber;
          cell.draggable = true;
          cell.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', JSON.stringify({ symbol, name, atomicNumber, color: periodColors[_period] }));
          });
          cell.addEventListener('click', () => showElementRecommendations(symbol));
        } else {
          cell.className = 'empty';
        }
        table.appendChild(cell);
      }
    }

    canvas.addEventListener('dragover', (e) => e.preventDefault());
    canvas.addEventListener('drop', (e) => {
      const json = e.dataTransfer.getData('text/plain');
      if (!json) return;
      const data = JSON.parse(json);
      const { symbol, color, atomicNumber } = data;
      createAtom(symbol, e.clientX - canvas.getBoundingClientRect().left - 20, e.clientY - canvas.getBoundingClientRect().top - 20, color, atomicNumber);
      symbolCount[symbol] = (symbolCount[symbol] || 0) + 1;
      updateFormula();
      updateRecommendations();
    });

    function createAtom(symbol, x, y, color, atomicNumber) {
      const atom = document.createElement('div');
      atom.className = 'atom';
      atom.textContent = symbol;
      atom.style.left = `${x}px`;
      atom.style.top = `${y}px`;
      atom.style.backgroundColor = color;
      atom.dataset.symbol = symbol;
      atom.dataset.id = nextId++;
      atom.dataset.atomicNumber = atomicNumber;
      atom.addEventListener('dblclick', () => {
        const atomSymbol = atom.dataset.symbol;
        symbolCount[atomSymbol]--;
        if (symbolCount[atomSymbol] <= 0) delete symbolCount[atomSymbol];
        canvasAtoms = canvasAtoms.filter(a => a !== atom);
        atom.remove();
        updateFormula(); updateBonds(); updateRecommendations();
      });
      enableDrag(atom);
      canvas.appendChild(atom);
      canvasAtoms.push(atom);
      updateBonds();
      return atom;
    }

    function enableDrag(el) {
      el.addEventListener('mousedown', (e) => {
        if (e.button !== 0 || e.detail > 1) return;
        const shiftX = e.clientX - el.getBoundingClientRect().left;
        const shiftY = e.clientY - el.getBoundingClientRect().top;
        el.style.zIndex = 1000;
        let isDragging = false;
        function moveAt(pageX, pageY) {
          isDragging = true;
          const canvasRect = canvas.getBoundingClientRect();
          let newX = pageX - canvasRect.left - shiftX;
          let newY = pageY - canvasRect.top - shiftY;
          el.style.left = newX + 'px';
          el.style.top = newY + 'px';
          const elRect = el.getBoundingClientRect();
          const elCenterX = elRect.left - canvasRect.left + elRect.width / 2;
          const elCenterY = elRect.top - canvasRect.top + elRect.height / 2;
          const isOutside = elCenterX < -(elRect.width / 4) || elCenterY < -(elRect.height / 4) || elCenterX > canvasRect.width + (elRect.width / 4) || elCenterY > canvasRect.height + (elRect.height / 4);
          el.style.opacity = isOutside ? '0.5' : '1';
          updateBonds();
        }
        const onMouseMove = (ev) => moveAt(ev.pageX, ev.pageY);
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', function onMouseUp() {
          document.removeEventListener('mousemove', onMouseMove);
          document.removeEventListener('mouseup', onMouseUp); // 자기 자신도 제거
          el.style.zIndex = 10;
          el.style.opacity = '1';
          if (!isDragging) { updateBonds(); updateRecommendations(); return; }
          const canvasRect = canvas.getBoundingClientRect();
          const elRect = el.getBoundingClientRect();
          const elCenterX = elRect.left - canvasRect.left + elRect.width / 2;
          const elCenterY = elRect.top - canvasRect.top + elRect.height / 2;
          if (elCenterX < -(elRect.width / 4) || elCenterY < -(elRect.height / 4) || elCenterX > canvasRect.width + (elRect.width / 4) || elCenterY > canvasRect.height + (elRect.height / 4)) {
            const symbol = el.dataset.symbol;
            symbolCount[symbol]--;
            if (symbolCount[symbol] <= 0) delete symbolCount[symbol];
            canvasAtoms = canvasAtoms.filter(atom => atom !== el);
            el.remove();
          }
          updateFormula(); updateBonds(); updateRecommendations();
        });
      });
    }

    function updateFormula() {
      if (Object.keys(symbolCount).length === 0) { formulaBox.textContent = '화학식을 여기에 보여줍니다'; return; }
      const sortedSymbolEntries = Object.entries(symbolCount).sort((a, b) => {
        const aNum = Object.keys(elementsData).find(key => elementsData[key][0] === a[0]);
        const bNum = Object.keys(elementsData).find(key => elementsData[key][0] === b[0]);
        return parseInt(aNum) - parseInt(bNum);
      });
      const formula = sortedSymbolEntries.map(([sym, count]) => `<span class="math-inline">\{sym\}</span>{count > 1 ? count : ''}`).join('');
      let compoundName = commonCompounds[formula] ? ` (${commonCompounds[formula].name})` : '';
      formulaBox.textContent = formula + compoundName;
    }

    function updateBonds() {
      document.querySelectorAll('.bond, .bond-label').forEach(el => el.remove());
      bonds = [];
      if (canvasAtoms.length < 2) return;
      for (let i = 0; i < canvasAtoms.length; i++) {
        for (let j = i + 1; j < canvasAtoms.length; j++) createBond(canvasAtoms[i], canvasAtoms[j]);
      }
    }

    function createBond(atom1, atom2) {
      if (!atom1.parentElement || !atom2.parentElement) return;
      const rect1 = atom1.getBoundingClientRect(), rect2 = atom2.getBoundingClientRect();
      const canvasRect = canvas.getBoundingClientRect();
      const x1 = rect1.left + rect1.width / 2 - canvasRect.left, y1 = rect1.top + rect1.height / 2 - canvasRect.top;
      const x2 = rect2.left + rect2.width / 2 - canvasRect.left, y2 = rect2.top + rect2.height / 2 - canvasRect.top;
      const dx = x2 - x1, dy = y2 - y1;
      const distance = Math.sqrt(dx * dx + dy * dy);
      const angle = Math.atan2(dy, dx) * 180 / Math.PI;
      const bondEl = document.createElement('div');
      bondEl.className = 'bond';
      bondEl.style.cssText = `width:<span class="math-inline">\{distance\}px; left\:</span>{x1}px; top:<span class="math-inline">\{y1\}px; transform\:rotate\(</span>{angle}deg);`;
      canvas.appendChild(bondEl); bonds.push(bondEl);
      const bondLabel = document.createElement('div');
      bondLabel.className = 'bond-label';
      bondLabel.textContent = `<span class="math-inline">\{atom1\.dataset\.symbol\}\-</span>{atom2.dataset.symbol}`;
      bondLabel.style.cssText = `left:<span class="math-inline">\{x1 \+ dx / 2 \- 15\}px; top\:</span>{y1 + dy / 2 - 8}px;`;
      canvas.appendChild(bondLabel); bonds.push(bondLabel);
    }

    function showElementRecommendations(symbol) {
      const compounds = elementCompounds[symbol] || [];
      if (compounds.length === 0) { recommendationsBox.innerHTML = `<h3>'${symbol}' 관련 화합물 추천</h3><p>추천 화합물이 없습니다.</p>`; return; }
      let html = `<h3>'${symbol}' 관련 화합물 추천</h3>`;
      compounds.forEach(formula => {
        html += `<div class="recommendation-item" data-formula="<span class="math-inline">\{formula\}"\></span>{formula}: ${commonCompounds[formula].name}</div>`;
      });
      recommendationsBox.innerHTML = html;
      addRecommendationClickEvents();
    }

    function updateRecommendations() {
      if (Object.keys(symbolCount).length === 0) { recommendationsBox.innerHTML = '<h3>화합물 추천</h3><p>원소를 먼저 추가하세요.</p>'; return; }
      const currentSymbols = Object.keys(symbolCount);
      let matchingCompounds = [];
      Object.entries(commonCompounds).forEach(([formula, compound]) => {
        if (currentSymbols.every(sym => Object.keys(compound.elements).includes(sym))) {
          matchingCompounds.push({ formula, name: compound.name });
        }
      });
      if (matchingCompounds.length === 0) { recommendationsBox.innerHTML = '<h3>화합물 추천</h3><p>추천 화합물이 없습니다.</p>'; return; }
      let html = '<h3>가능한 화합물 추천</h3>';
      matchingCompounds.forEach(({ formula, name }) => {
        html += `<div class="recommendation-item" data-formula="<span class="math-inline">\{formula\}"\></span>{formula}: ${name}</div>`;
      });
      recommendationsBox.innerHTML = html;
      addRecommendationClickEvents();
    }

    function addRecommendationClickEvents() {
      document.querySelectorAll('.recommendation-item').forEach(item => {
        item.addEventListener('click', () => {
          const formula = item.dataset.formula;
          const compound = commonCompounds[formula];
          resetCanvas();
          let posX = 50, posY = 100;
          Object.entries(compound.elements).forEach(([sym, count]) => {
            const atomicNumStr = Object.keys(elementsData).find(key => elementsData[key][0] === sym);
            if (!atomicNumStr) return;
            const atomicNumber = parseInt(atomicNumStr);
            const [_s, _n, _g, period] = elementsData[atomicNumber];
            const color = periodColors[period];
            for (let i = 0; i < count; i++) {
              createAtom(sym, posX, posY, color, atomicNumber);
              symbolCount[sym] = (symbolCount[sym] || 0) + 1;
              posX += 60; if (posX > canvas.offsetWidth - 60) { posX = 50; posY += 60; }
            }
          });
          updateFormula();
        });
      });
    }

    function resetCanvas() {
      document.querySelectorAll('.atom, .bond, .bond-label').forEach(el => el.remove());
      canvasAtoms = []; bonds = []; symbolCount = {}; nextId = 1;
      updateFormula(); updateRecommendations();
    }

    function saveConfiguration() {
      const configuration = {
        atoms: canvasAtoms.map(atom => ({
          symbol: atom.dataset.symbol, x: parseFloat(atom.style.left), y: parseFloat(atom.style.top),
          color: atom.style.backgroundColor, atomicNumber: atom.dataset.atomicNumber
        })),
        formula: formulaBox.textContent, nextId: nextId
      };
      localStorage.setItem('chemSimulatorConfig', JSON.stringify(configuration));
      alert('현재 상태가 저장되었습니다.');
    }

    function loadConfiguration() {
      const savedConfig = localStorage.getItem('chemSimulatorConfig');
      if (!savedConfig) return;
      const configuration = JSON.parse(savedConfig);
      resetCanvas();
      nextId = configuration.nextId || 1;
      configuration.atoms.forEach(atomData => {
        createAtom(atomData.symbol, atomData.x, atomData.y, atomData.color, atomData.atomicNumber);
        symbolCount[atomData.symbol] = (symbolCount[atomData.symbol] || 0) + 1;
      });
      updateFormula(); updateRecommendations();
    }

    saveBtn.addEventListener('click', saveConfiguration);
    resetBtn.addEventListener('click', resetCanvas);

    window.addEventListener('load', () => {
      updateRecommendations();
      if (localStorage.getItem('chemSimulatorConfig')) loadConfiguration();
    });
  </script>
</body>
</html>
"""

# Streamlit 페이지 설정 (선택 사항)
st.set_page_config(layout="wide") # 넓은 레이아웃 사용

st.title("Streamlit 화학식 시뮬레이터")

# HTML 컴포넌트 삽입
# height는 iframe의 높이를 지정합니다. 내용에 맞게 적절히 조절해야 합니다.
# scrolling=True를 하면 내용이 넘칠 경우 스크롤바가 생깁니다.
st.html(html_code, height=700, scrolling=True)

# 여기에 다른 Streamlit 위젯들을 추가할 수도 있습니다.
st.sidebar.header("Streamlit Controls")
name = st.sidebar.text_input("Your Name")
if name:
    st.sidebar.write(f"Hello, {name}!")
