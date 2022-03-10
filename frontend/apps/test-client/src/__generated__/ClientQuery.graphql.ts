/**
 * @generated SignedSource<<5d38ee389bf013e44d6c90dae953cb51>>
 * @lightSyntaxTransform
 * @nogrep
 */

/* tslint:disable */
/* eslint-disable */
// @ts-nocheck

import { ConcreteRequest, Query } from 'relay-runtime';
export type PatientSex = "NONE" | "MALE" | "FEMALE" | "DIVERSE" | "%future added value";
export type PatientStatus = "NEW" | "RECORDING" | "DIAGNOSIS" | "%future added value";
export type ClientQuery$variables = {};
export type ClientQuery$data = {
  readonly me: {
    readonly id: string;
    readonly name: string;
    readonly age: number;
  } | null;
  readonly allPatients: ReadonlyArray<{
    readonly id: string;
    readonly sex: PatientSex;
    readonly birthday: string;
    readonly concern: string;
    readonly admissionDate: string;
    readonly status: PatientStatus;
  }>;
};
export type ClientQuery = {
  variables: ClientQuery$variables;
  response: ClientQuery$data;
};

const node: ConcreteRequest = (function(){
var v0 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "id",
  "storageKey": null
},
v1 = [
  {
    "alias": null,
    "args": null,
    "concreteType": "User",
    "kind": "LinkedField",
    "name": "me",
    "plural": false,
    "selections": [
      (v0/*: any*/),
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "name",
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "age",
        "storageKey": null
      }
    ],
    "storageKey": null
  },
  {
    "alias": null,
    "args": null,
    "concreteType": "Patient",
    "kind": "LinkedField",
    "name": "allPatients",
    "plural": true,
    "selections": [
      (v0/*: any*/),
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
    "argumentDefinitions": [],
    "kind": "Fragment",
    "metadata": null,
    "name": "ClientQuery",
    "selections": (v1/*: any*/),
    "type": "Query",
    "abstractKey": null
  },
  "kind": "Request",
  "operation": {
    "argumentDefinitions": [],
    "kind": "Operation",
    "name": "ClientQuery",
    "selections": (v1/*: any*/)
  },
  "params": {
    "cacheID": "1ae2403d318bf46e5ebc616e2081c654",
    "id": null,
    "metadata": {},
    "name": "ClientQuery",
    "operationKind": "query",
    "text": "query ClientQuery {\n  me {\n    id\n    name\n    age\n  }\n  allPatients {\n    id\n    sex\n    birthday\n    concern\n    admissionDate\n    status\n  }\n}\n"
  }
};
})();

(node as any).hash = "bd79a533422591821d44408be03ec142";

export default node;
