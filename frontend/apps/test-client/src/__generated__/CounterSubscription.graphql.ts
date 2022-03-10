/**
 * @generated SignedSource<<dc13ceab1009b259d0a9572fb0f04d9c>>
 * @lightSyntaxTransform
 * @nogrep
 */

/* tslint:disable */
/* eslint-disable */
// @ts-nocheck

import { ConcreteRequest, GraphQLSubscription } from 'relay-runtime';
export type PatientSex = "NONE" | "MALE" | "FEMALE" | "DIVERSE" | "%future added value";
export type PatientStatus = "NEW" | "RECORDING" | "DIAGNOSIS" | "%future added value";
export type CounterSubscription$variables = {
  upto: number;
};
export type CounterSubscription$data = {
  readonly data: ReadonlyArray<{
    readonly id: string;
    readonly sex: PatientSex;
    readonly birthday: string;
    readonly concern: string;
    readonly admissionDate: string;
    readonly status: PatientStatus;
  }> | null;
};
export type CounterSubscription = {
  variables: CounterSubscription$variables;
  response: CounterSubscription$data;
};

const node: ConcreteRequest = (function(){
var v0 = [
  {
    "defaultValue": null,
    "kind": "LocalArgument",
    "name": "upto"
  }
],
v1 = [
  {
    "alias": null,
    "args": [
      {
        "kind": "Variable",
        "name": "upto",
        "variableName": "upto"
      }
    ],
    "concreteType": "Patient",
    "kind": "LinkedField",
    "name": "data",
    "plural": true,
    "selections": [
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "id",
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "sex",
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "birthday",
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "concern",
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "admissionDate",
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "status",
        "storageKey": null
      }
    ],
    "storageKey": null
  }
];
return {
  "fragment": {
    "argumentDefinitions": (v0/*: any*/),
    "kind": "Fragment",
    "metadata": null,
    "name": "CounterSubscription",
    "selections": (v1/*: any*/),
    "type": "Subscription",
    "abstractKey": null
  },
  "kind": "Request",
  "operation": {
    "argumentDefinitions": (v0/*: any*/),
    "kind": "Operation",
    "name": "CounterSubscription",
    "selections": (v1/*: any*/)
  },
  "params": {
    "cacheID": "8fece710a5f023383b3fba0724c4f954",
    "id": null,
    "metadata": {},
    "name": "CounterSubscription",
    "operationKind": "subscription",
    "text": "subscription CounterSubscription(\n  $upto: Int!\n) {\n  data(upto: $upto) {\n    id\n    sex\n    birthday\n    concern\n    admissionDate\n    status\n  }\n}\n"
  }
};
})();

(node as any).hash = "8bc56cde59820539bcb1bb8f612b8335";

export default node;
