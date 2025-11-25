# GSBPD2 Development Roadmap
## Strategic Plan for Sports Betting Prediction Dashboard

**Created**: 2025-11-25
**Status**: Active Development
**Current Version**: 1.1 (UI Redesigned + Dependencies Fixed)

---

## 🎯 Vision

Build a **professional-grade sports betting intelligence platform** that combines:
- Real-time NFL data & odds
- AI-powered predictions with transparency (SHAP)
- Smart Same Game Parlay (SGP) suggestions
- Automated data extraction from screen recordings
- Continuous learning from your betting history

---

## 📍 Current State (v1.1)

### ✅ What We Have
- **Frontend**: Modern React 19 UI with futuristic outer space theme
- **Backend**: FastAPI with XGBoost ML model + SHAP explainability
- **Storage**: Memvid video-based compression + JSON backup
- **Infrastructure**: Fully running locally (ports 8000 + 5173)
- **Dependencies**: All Python/Node packages installed

### 🟡 What's Mock
- NFL games list (3 hardcoded teams)
- Video OCR detection (fake game extraction)
- KC DaCRE8TOR insights (template-based, not real AI)
- SGP prop odds (hardcoded, not from sportsbook)

---

## 🗺️ Strategic Phases

### **Phase 1: Foundation Solidification** (NOW → 1 Week)
**Goal**: Make the core system production-ready with real data

#### Priority 1.1: Real Data Integration
- [ ] **The Odds API Integration** (30 min)
  - Sign up for free API key (500 requests/month)
  - Set `ODDS_API_KEY` environment variable
  - Test with live NFL games endpoint
  - Verify real odds display in GameSelector

- [ ] **Model Persistence** (1 hour)
  - Implement model saving/loading (currently retrains on restart)
  - Add versioning for models
  - Create model evaluation metrics storage
  - File: backend/model.py:31

- [ ] **Configuration Management** (30 min)
  - Create `.env` file for environment variables
  - Add `.env.example` template
  - Document all configuration options
  - Use `python-dotenv` for loading

#### Priority 1.2: Testing & Validation
- [ ] **End-to-End Testing** (2 hours)
  - Test full prediction flow with real games
  - Test bet placement → resolution → retraining cycle
  - Test video ingest (even with mock OCR)
  - Test SGP generation
  - Document any bugs found

- [ ] **Data Validation** (1 hour)
  - Add Pydantic validation for all API inputs
  - Add frontend form validation
  - Handle edge cases (missing data, API errors)
  - Improve error messages

#### Priority 1.3: Documentation Updates
- [ ] **README.md Enhancement** (1 hour)
  - Add "Quick Start" section with exact commands
  - Document environment variables
  - Add screenshots of UI
  - Include troubleshooting section

- [ ] **API Documentation** (30 min)
  - Enhance FastAPI auto-docs (/docs endpoint)
  - Add request/response examples
  - Document error codes

**Deliverable**: Fully functional system with real NFL data and proper error handling

---

### **Phase 2: Intelligence Upgrade** (1-2 Weeks)
**Goal**: Enhance AI capabilities and make predictions more accurate

#### Priority 2.1: Real OCR Implementation
- [ ] **Research OCR Solutions** (2 hours)
  - Evaluate Tesseract vs EasyOCR vs Cloud Vision API
  - Test on sample screen recordings
  - Choose best approach for sports scores

- [ ] **Basic OCR Integration** (4 hours)
  - Implement frame sampling (every N seconds)
  - Text detection and extraction
  - Team name recognition (fuzzy matching against NFL teams list)
  - Score parsing (regex patterns)
  - File: backend/services/knowledge_base.py:17-73

- [ ] **OCR Quality Improvements** (3 hours)
  - Add pre-processing (contrast, brightness, noise reduction)
  - Implement confidence scoring
  - Add manual correction UI for low-confidence detections
  - Store OCR results for debugging

#### Priority 2.2: Enhanced Predictions
- [ ] **Feature Engineering** (3 hours)
  - Research additional features (weather, injuries, rest days, matchup history)
  - Scrape or API-integrate historical game data
  - Add features to model input
  - Retrain with expanded feature set

- [ ] **Model Improvements** (4 hours)
  - Hyperparameter tuning (GridSearchCV)
  - Try alternative algorithms (LightGBM, CatBoost)
  - Ensemble methods (combine multiple models)
  - Add confidence intervals to predictions

- [ ] **Real AI Insights** (2 hours)
  - Integrate OpenAI GPT-4 or Anthropic Claude API
  - Create prompt template for insights
  - Include SHAP values in context
  - Generate personalized betting advice
  - File: backend/grok.py (rename to insights.py and rewrite)

#### Priority 2.3: Advanced SGP Engine
- [ ] **Real Prop Odds Integration** (4 hours)
  - Research sportsbook APIs (DraftKings, FanDuel, etc.)
  - Integrate player prop odds
  - Update correlation matrix based on real data
  - File: backend/services/sgp_engine.py

- [ ] **Correlation Analysis** (3 hours)
  - Analyze historical data for true correlations
  - Machine learning for correlation discovery
  - Dynamic correlation matrix (not hardcoded)
  - Backtest SGP suggestions against actual outcomes

**Deliverable**: Intelligent system with real OCR, better predictions, and smarter SGP suggestions

---

### **Phase 3: Scale & Polish** (2-3 Weeks)
**Goal**: Make the system robust, scalable, and delightful to use

#### Priority 3.1: User Experience
- [ ] **Onboarding Flow** (2 hours)
  - Welcome screen explaining features
  - Interactive tutorial
  - Sample prediction walkthrough
  - First-time setup wizard

- [ ] **Advanced Visualizations** (4 hours)
  - Historical prediction accuracy chart
  - Win rate over time
  - Feature importance trends
  - SGP success rate analysis

- [ ] **Mobile Responsiveness** (3 hours)
  - Test on mobile devices
  - Adjust layouts for small screens
  - Touch-friendly interactions
  - Consider Progressive Web App (PWA)

#### Priority 3.2: Performance Optimization
- [ ] **Backend Optimization** (3 hours)
  - Add Redis caching for API responses
  - Optimize Memvid rebuild (only when necessary)
  - Database migration planning (if needed)
  - Background task queue (Celery)

- [ ] **Frontend Optimization** (2 hours)
  - Code splitting for faster initial load
  - Lazy loading for components
  - Image optimization
  - Bundle size analysis

#### Priority 3.3: Production Deployment
- [ ] **Backend Deployment** (4 hours)
  - Choose platform (Railway, Heroku, AWS)
  - Set up CI/CD (GitHub Actions)
  - Configure environment variables
  - SSL/HTTPS setup
  - Health check endpoints

- [ ] **Frontend Deployment** (2 hours)
  - Deploy to Vercel or Netlify
  - Configure custom domain
  - Environment-specific API URLs
  - Analytics integration (optional)

- [ ] **Database Migration** (6 hours)
  - Evaluate if Memvid should be supplemented/replaced
  - PostgreSQL setup for structured data
  - S3 for video storage
  - Migration scripts

**Deliverable**: Production-ready application accessible online

---

### **Phase 4: Advanced Features** (Future)
**Goal**: Differentiate with unique capabilities

#### Priority 4.1: Multi-Sport Support
- Extend to NBA, MLB, NHL
- Sport-specific models
- Cross-sport insights

#### Priority 4.2: Social Features
- User authentication
- Betting communities
- Leaderboards
- Share predictions

#### Priority 4.3: Advanced Analytics
- Portfolio optimization
- Bankroll management AI
- Risk analysis
- Historical trend analysis

#### Priority 4.4: Automation
- Automated bet placement (with user approval)
- Daily email reports
- Slack/Discord notifications
- Alert system for high-confidence picks

---

## 🎲 Strategic Decision Points

### Decision 1: Real-Time Odds vs Daily Refresh
**Options**:
- **A**: WebSocket connection for live odds updates (complex, expensive API calls)
- **B**: Refresh odds every 15 minutes (simpler, within free tier)
- **C**: Manual refresh button (simplest, cheapest)

**Recommendation**: Start with (B), upgrade to (A) if demand justifies cost

### Decision 2: OCR Quality vs Cost
**Options**:
- **A**: Cloud Vision API (best quality, costs money)
- **B**: Tesseract (free, good quality, requires tuning)
- **C**: Manual data entry UI (no OCR cost, user effort)

**Recommendation**: Start with (B), offer (C) as backup for low-confidence detections

### Decision 3: Data Storage Strategy
**Options**:
- **A**: Keep Memvid only (unique, but limited query capabilities)
- **B**: Add PostgreSQL alongside Memvid (hybrid approach)
- **C**: Migrate fully to PostgreSQL (traditional, well-supported)

**Recommendation**: Keep (A) for now, add (B) in Phase 3 for complex queries

### Decision 4: Monetization (If Applicable)
**Options**:
- **A**: Personal use only (free forever)
- **B**: Subscription service ($9.99/month)
- **C**: Freemium model (basic free, premium features paid)
- **D**: Affiliate marketing (link to sportsbooks)

**Recommendation**: Decide after Phase 2 completion based on results

---

## 📊 Success Metrics

### Phase 1 Success Criteria
- [ ] 100% uptime for 7 days straight
- [ ] Real NFL games displaying correctly
- [ ] Zero errors in prediction flow
- [ ] Model persists across restarts

### Phase 2 Success Criteria
- [ ] OCR accuracy > 80% on test videos
- [ ] Prediction accuracy improvement (baseline vs current)
- [ ] AI insights rated 4+ stars (if user feedback implemented)
- [ ] SGP suggestions validated against actual correlations

### Phase 3 Success Criteria
- [ ] Page load time < 2 seconds
- [ ] Mobile experience rated excellent
- [ ] 99.9% uptime (if deployed)
- [ ] Zero security vulnerabilities

---

## 🚧 Known Blockers & Risks

### Technical Risks
- **Odds API Rate Limits**: Free tier may not be enough → Monitor usage, plan upgrade
- **OCR Accuracy**: Sports scores in videos can be tricky → Spend time on pre-processing
- **Model Overfitting**: Small training dataset → Need more real bet data

### Business Risks
- **API Cost**: Scaling may require paid APIs → Budget for cloud costs
- **Legal**: Sports betting regulation varies by state → Consult lawyer if monetizing
- **Data Availability**: Sportsbooks may change APIs → Have backup data sources

### Operational Risks
- **Solo Developer**: No backup if you're unavailable → Document everything
- **Technical Debt**: Fast development = messy code → Allocate refactor time

---

## 🎯 Next Steps (Immediate Action Items)

### This Week (Phase 1.1)
1. **Monday**: Get Odds API key, integrate real games
2. **Tuesday**: Implement model persistence
3. **Wednesday**: Create .env setup, test end-to-end
4. **Thursday**: Update documentation
5. **Friday**: Demo to yourself, note issues

### Next 2 Weeks (Phase 1.2 + 2.1)
- Week 2: Testing, validation, bug fixes
- Week 3: OCR research and basic implementation

### This Month (Complete Phase 1 + Start Phase 2)
- Solid foundation with real data
- Begin intelligent features

---

## 📝 Notes & Ideas

### Ideas to Explore
- Browser extension for instant odds lookup
- Telegram bot for predictions on-the-go
- Historical game database scraping
- Live betting adjustments (in-game predictions)
- Arbitrage opportunity detection

### Community Features (Future)
- Reddit integration (scrape r/sportsbook for sentiment)
- Twitter sentiment analysis
- Expert picks aggregation
- Contrarian betting indicators

### Technical Experiments
- LSTM for time-series predictions
- Reinforcement learning for bankroll management
- Graph neural networks for team relationships
- Genetic algorithms for SGP optimization

---

**Ready to Build!** 🚀

Let's start with Phase 1.1: Real Data Integration. Which would you like to tackle first?
1. Get The Odds API key for real games
2. Implement model persistence
3. Something else?
