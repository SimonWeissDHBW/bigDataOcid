FROM node:16 AS UI

COPY ./vue_frontend/ ./vue_frontend/

RUN cd vue_frontend && npm install && npm run build

FROM node:16 AS SERVER

COPY ./express_backend/ ./express_backend/
COPY --from=UI ./vue_frontend/dist/ ./express_backend/dist/
RUN cd express_backend && npm install

EXPOSE 3000

CMD ["node", "./express_backend/app.js"]