import { commitMutation, graphql } from "react-relay";
import environment from "../environment";
import { newCardMutation } from "./__generated__/newCardMutation.graphql";

const mutation = graphql`
  mutation newCardMutation(
    $author: String!
    ) {
    newCard(input: {author: $author}) {
      ok
      card {
        id
        author
        date
      }
    }
  }
`;

// const configs: DeclarativeMutationConfig[] = [{
//   type: "RANGE_ADD",
//   parentID: "client:root:allCards",
//   edgeName: "edge",
// }];

export function newCard(author: string) {
  const variables = { author };
  commitMutation<newCardMutation>(environment, {
    mutation,
    variables,
    updater: (store, data) => {
      const root = store.getRootField("newCard");
      console.log(root);


    },
    onCompleted: (res, err) => {
      console.log(res.newCard?.ok);
    },
    onError: (err) => console.error(err),
  });
}
