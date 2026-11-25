
const app = require('./app');
const { Eureka } = require('eureka-js-client');

const PORT = Number(process.env.PORT) || 8085;

const eurekaClient = new Eureka({
  instance: {
    app: 'MEETING',
    instanceId: `MEETING:localhost:${PORT}`,
    hostName: 'localhost',
    ipAddr: '127.0.0.1',
    status: 'UP',

    port: {
      '$': PORT,
      '@enabled': 'true'
    },

    vipAddress: 'MEETING',

    // URLs de santé et d'information
    healthCheckUrl: `http://localhost:${PORT}/health`,
    statusPageUrl: `http://localhost:${PORT}/info`,

    dataCenterInfo: {
      '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
      name: 'MyOwn'
    }
  },

  eureka: {
    host: 'localhost',
    port: 8761,
    servicePath: '/eureka/apps/'
  }
});

const server = app.listen(PORT, () => {
  console.log(`meeting microservice running on http://localhost:${PORT}`);
  console.log(`Swagger UI: http://localhost:${PORT}/swagger-ui`);

  eurekaClient.start();
});

// Arrêter proprement le client Eureka
process.on('SIGINT', () => {
  eurekaClient.stop();
  server.close(() => process.exit(0));
});

process.on('SIGTERM', () => {
  eurekaClient.stop();
  server.close(() => process.exit(0));
});
