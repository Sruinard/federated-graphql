import { ApolloServer } from "apollo-server";
import { ApolloGateway } from "@apollo/gateway";

const gateway = new ApolloGateway({
  serviceList: [
    {
      name: "catalogue",
      url: "https://catalogue.wittypebble-179ef70d.westeurope.azurecontainerapps.io/graphql",
      // url: "http://catalogue:8000/graphql"
    },
    {
      name: "enterprise",
      url: "https://enterprise.wittypebble-179ef70d.westeurope.azurecontainerapps.io/graphql",
      // url: "http://enterprise:8800/graphql"
    },
  ],
  experimental_pollInterval: 2000,
});

const server = new ApolloServer({
  gateway,
  subscriptions: false,
});

server
  .listen({ port: 7000 })
  .then(({ url }) => {
    console.info(`🚀 Gateway available at ${url}`);
  })
  .catch((err) => console.error("❌ Unable to start gateway", err));
