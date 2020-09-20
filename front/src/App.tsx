import React from 'react';
import './App.scss';
import { QueryRenderer, graphql } from "react-relay";
import environment from './_lib/environment';
import { AppQuery } from './__generated__/AppQuery.graphql';
import Card from "./components/Card";

function App() {
  return (
    <div className="App">
      <div className="header">
        <h1>Story Board</h1>
        <p>by</p>
        <input placeholder="누가 작성중인가요?" />
      </div>
      <QueryRenderer<AppQuery>
        query={graphql`
            query AppQuery {
              allCards {
                edges {
                  node {
                    ...Card_card
                  }
                }
              }
            }
          `}
        variables={{}}
        environment={environment}
        render={({ props, error }) => {
          const edges = props?.allCards?.edges;
          return edges && edges.map((edge, i) => edge && <Card card={edge.node} key={i} />)
        }}
      />
    </div>
  );
}

export default App;