# Development Notes

## Architecture Decisions

### Backend (FastAPI)
- **Async/Await**: Used throughout for better performance
- **SQLAlchemy Async**: Modern async ORM implementation
- **Pydantic v2**: Strong type validation
- **SQLite default**: Easy setup, can switch to PostgreSQL

### Frontend (Vue 3)
- **Composition API**: Modern, more flexible than Options API
- **Pinia**: Lightweight state management
- **Tailwind CSS**: Utility-first, no CSS-in-JS overhead
- **Web Speech API**: Browser-native, no external dependencies

### Question Flow Logic
The questionnaire uses a conditional flow system:
1. Welcome screen
2. Tester info (name, sample)
3. Primary flavor category selection
4. Specific flavor notes (based on category)
5. Intensity, aftertaste, body, acidity
6. Balance and overall impression
7. Additional notes

Flow is defined in `backend/services.py` in the `QUESTION_FLOW` dictionary.

## Key Components

### Backend
- `main.py`: FastAPI app with all endpoints
- `database.py`: Async DB setup
- `models.py`: SQLAlchemy models (Session, Answer, Question)
- `schemas.py`: Pydantic request/response models
- `services.py`: Business logic, CSV parsing, question flow

### Frontend
- `stores/feedback.js`: Pinia store for session state
- `composables/useSpeech.js`: Web Speech API wrapper
- `components/QuestionPanel.vue`: Displays questions and options
- `components/VoicePanel.vue`: Microphone and voice interaction
- `views/HomeView.vue`: Landing page
- `views/FeedbackView.vue`: Main feedback interface
- `views/CompletionView.vue`: Success page with confetti

## Adding New Features

### New Question Type
1. Add to `backend/services.py` in `questions_data`
2. Update `frontend/components/QuestionPanel.vue` to handle new type
3. Add to question flow logic

### New Flavor Category
1. Edit `Flavor.csv`
2. Restart backend (it loads CSV on startup)
3. Update `QUESTION_FLOW` in `services.py` if conditional logic needed

### Custom Animations
Edit `frontend/src/style.css` and `tailwind.config.js`

## Performance Optimization

### Backend
- Use Redis for caching (future enhancement)
- Add connection pooling for PostgreSQL
- Implement rate limiting

### Frontend
- Lazy load routes: `component: () => import('./views/...')`
- Use `v-show` instead of `v-if` for frequent toggles
- Debounce voice input processing

## Security Considerations

### Production Checklist
- [ ] Enable HTTPS (required for Web Speech API)
- [ ] Add authentication/authorization
- [ ] Implement CSRF protection
- [ ] Rate limit API endpoints
- [ ] Sanitize user inputs
- [ ] Add CSP headers
- [ ] Enable CORS only for specific origins
- [ ] Use environment variables for secrets
- [ ] Regular dependency updates

## Testing Strategy

### Backend Tests
- Unit tests for services
- Integration tests for API endpoints
- Database migration tests

### Frontend Tests
- Component unit tests (Vitest)
- E2E tests (Playwright/Cypress)
- Accessibility tests

### Manual Testing
- Test in Chrome, Edge, Safari
- Test on mobile devices
- Test with screen readers
- Test voice recognition accuracy

## Deployment

### Backend (Production)
```bash
# Using Gunicorn + Uvicorn workers
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Or using Docker
docker build -t coffee-backend ./backend
docker run -p 8000:8000 coffee-backend
```

### Frontend (Production)
```bash
# Build static files
npm run build

# Serve with nginx or any static host
# Deploy to Vercel, Netlify, or AWS S3
```

### Environment Variables (Production)
- Set `DATABASE_URL` to PostgreSQL connection string
- Set `VITE_API_URL` to production API URL
- Enable HTTPS
- Set appropriate CORS origins

## Common Issues

### Issue: Voice recognition stops immediately
**Solution**: Check microphone permissions, ensure HTTPS

### Issue: Backend can't find Flavor.csv
**Solution**: Ensure CSV is in project root, check path in `services.py`

### Issue: CORS errors
**Solution**: Update `allow_origins` in `main.py`

### Issue: Frontend can't connect to backend
**Solution**: Check `VITE_API_URL` in `.env` file

## Future Enhancements

- [ ] Multi-language support (i18n)
- [ ] PDF report generation with charts
- [ ] Audio recording save feature
- [ ] Admin dashboard for analytics
- [ ] Batch session management
- [ ] Export to CSV/Excel
- [ ] Real-time collaboration
- [ ] Mobile app (React Native/Flutter)
- [ ] Offline mode with sync
- [ ] AI-powered flavor suggestions
- [ ] Integration with coffee databases
- [ ] Social sharing features

## Resources

- [Vue 3 Docs](https://vuejs.org/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [Tailwind CSS](https://tailwindcss.com/)
- [Pinia](https://pinia.vuejs.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
