import {
  Environment,
  FetchFunction,
  GraphQLResponse,
  Network,
  RecordSource,
  Store,
} from 'relay-runtime';
import { GRAPHQL_ENDPOINT } from "./endpoint";

const fetchQuery: FetchFunction = async (operation, variables): Promise<GraphQLResponse> => {
  try {
    const response = await fetch(GRAPHQL_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: operation.text,
        variables,
      }),
    });
    return await response.json();
  } catch (e) {
    return { errors: [new Error('네트워크 요청이 실패했습니다. ' + e.message)], data: undefined };
  }
}

const environment = new Environment({
  network: Network.create(fetchQuery),
  store: new Store(new RecordSource()),
});

export default environment;