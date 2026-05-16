// ==========================================
// ゲーム②: 素数ハンター
// ==========================================
class HunterGame {
  ArrayList<NumberBubble> bubbles;
  int timer = 1000;
  boolean showingExplanation = false; // 解説モードフラグ
  
  HunterGame() {
    setupStage();
  }
  int n;
  void setupStage() {
    bubbles = new ArrayList<NumberBubble>();
    // 難易度に応じて数や速度を変える
    for (int i = 0; i < int(10*(0.5*(level%3)+1)); i++) {
      if (level%3 == 0){
        n = int(random(2, 50));
        timer = 3000;
      } else if (level%3 == 1){
        n = int(random(10, 100));
        timer = 2000;
      } else {
        n = int(random(30, 150));
        timer = 1000;
      }
      bubbles.add(new NumberBubble(n, random(5, width-5), random(65, height-5)));
    }
    showingExplanation = false;
  }
  
  void run() {
    if (showingExplanation) {
      drawExplanation();
      return;
    }

    timer--;
    if (timer <= 0) checkTimeUp(); // 時間切れ判定

    // 更新と描画
    boolean primeExists = false;
    for (NumberBubble b : bubbles) {
      b.update();
      // ヒント表示（時間経過で簡易表示）
      if (hintEnabled && timer < 500) b.hint = true;
      b.display(b.miss, b.hint, b.isPrimeVal);
      if (b.isPrimeVal && b.active) primeExists = true;
    }
    
    // UI
    fill(244); rect(0, 0, width, 60);
    fill(0); textAlign(LEFT);
    text("Time: " + timer, 20, 40);
    text("Life: " + life, 200, 40);
    text((isLifeMode ? "" : "Streak: " + consecutiveWins + "/5"), width/2, 40);
    text("Score: " + score, width/2 + 200, 40);
    
    // 素数を全部消せたらクリア
    if (!primeExists) {
      handleWin();
    }
    if (life <= 0 && !showingExplanation){
        currentState = STATE_GAME_OVER;
    }
  }
  
  void handleClick(float mx, float my) {
    if (showingExplanation) {
      // 解説中ならクリックで次へ
      setupStage();
      return;
    }
    
    for (NumberBubble b : bubbles) {
      if (b.active && dist(mx, my, b.x, b.y) < b.r) {
        if (b.isPrimeVal) {
          b.active = false; // 正解：消す
          score += 100;
          count += 1;
        } else {
          // 不正解：合成数をクリック
          handleFail();
          if (isLifeMode){
            b.miss = true;
          }
          break;
        }
      }
    }
    if (1 < count){
      score += (count-1) * 10000;
      count = 0;
    }
  }
  
  void handleWin() {
    consecutiveWins++;
    if (!isLifeMode && consecutiveWins >= GOAL_STREAK) {
      currentState = STATE_GAME_CLEAR;
    } else {
      score += timer * ((level%3)+1) * 0.3;
      setupStage(); // 解説なしで次へ
    }
  }
  
  void checkTimeUp() {
    // 素数が残っているか確認
    boolean primeRemains = false;
    for (NumberBubble b : bubbles) {
      if (b.active && b.isPrimeVal) primeRemains = true;
    }
    
    if (primeRemains) handleFail();
    else setupStage(); // 素数がないなら一応セーフ
  }

  void handleFail() {
    life--;
    if (isLifeMode && life <= 0) {
      currentState = STATE_GAME_OVER;
    } else if (!isLifeMode) {
      consecutiveWins = 0;
    }
    showingExplanation = true; // 解説へ
  }
  
  void drawExplanation() {
    background(50);
    textAlign(CENTER);
    fill(255); text("OOPS! Look at the Primes (Red). Click to Next.", width/2, 50);
    
    for (NumberBubble b : bubbles) {
      // 解説時は動きを止めて表示
      if (b.active){
        if (b.isPrimeVal) fill(255, 100, 100); // 素数は赤
        else fill(200);                        // 合成数はグレー
        ellipse(b.x, b.y, b.r*2, b.r*2);
        fill(0); text(b.val, b.x, b.y + 8);
      }
    }
  }
}

// 数字ボールクラス
class NumberBubble {
  float x, y, vx, vy, r;
  int val;
  boolean isPrimeVal;
  boolean active = true;
  boolean miss = false;
  boolean hint = false;
  
  NumberBubble(int v, float _x, float _y) {
    val = v; x = _x; y = _y;
    vx = random(1,2); vy = random(1,2);
    if (int(random(2))==1){
      vx *= -1;
    } if (int(random(2))==1){
      vy *= -1;
    }
    r = 25;
    isPrimeVal = isPrime(val);
  }
  
  void update() {
    x += vx; y += vy;
    // 跳ね返り処理
    //if (x < r*1.5 || x > width - r*1.5) vx *= -1;
    if ((x < r*1.5 && vx < 0) || (width - r*1.5 < x && 0 < vx)) vx *= -1;
    //if (y < r*1.5 || y > height - r*1.5) vy *= -1;
    if ((y < r*1.5 + 60 && vy < 0) || (height - r*1.5 < y && 0 < vy)) vy *= -1;
  }
  
  void display(boolean miss, boolean hint, boolean isPrimeVal) {
    if (!active) return;
    if (miss){
      fill(255, 100, 100); // 間違えたものは赤で表示
    } else if (hint && isPrimeVal){
      fill(255, 240, 240);
    } else{
      fill(255);
    } 
    stroke(0);
    ellipse(x, y, r*2, r*2);
    fill(0); textAlign(CENTER);
    text(val, x, y + 8);
  }
}
