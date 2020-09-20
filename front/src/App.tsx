import React from 'react';
import './App.scss';
import { QueryRenderer, graphql } from "react-relay";
import environment from './_lib/environment';
import { AppQuery } from './__generated__/AppQuery.graphql';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <QueryRenderer<AppQuery>
          query={graphql`
            query AppQuery {
              allCards {
                edges {
                  node {
                    id
                    title
                  }
                }
              }
            }
          `}
          variables={{}}
          environment={environment}
          render={({ props, error }) => { console.log(props); return (<h1>hi</h1>) }}
        />
      </header>
    </div>
  );
}

export default App;