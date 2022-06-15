import { ApolloServer } from "apollo-server";
import { ApolloGateway } from "@apollo/gateway";

const gateway = new ApolloGateway({
  serviceList: [
    {
      name: "account",
      url: "https://account.wittypebble-179ef70d.westeurope.azurecontainerapps.io/graphql",
      // url: "http://catalogue:8000/graphql"
    },
    {
      name: "payments",
      url: "https://payments.wittypebble-179ef70d.westeurope.azurecontainerapps.io/graphql",
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
