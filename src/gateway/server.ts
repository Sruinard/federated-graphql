import { ApolloServer } from "apollo-server";
import { ApolloGateway } from "@apollo/gateway";

const gateway = new ApolloGateway({
  serviceList: [
    {
      name: "founders",
      url: process.env.FOUNDERS_ENDPOINT
      // url: "http://catalogue:8000/graphql"
    },
    {
      name: "companies",
      url: process.env.COMPANIES_ENDPOINT
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
