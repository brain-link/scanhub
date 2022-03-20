/**
 * @generated SignedSource<<5a7bb31e401516879e2642b96425c13b>>
 * @lightSyntaxTransform
 * @nogrep
 */

/* tslint:disable */
/* eslint-disable */
// @ts-nocheck

import { ConcreteRequest, Query } from 'relay-runtime';
export type PatientSex = "NONE" | "MALE" | "FEMALE" | "DIVERSE" | "%future added value";
export type PatientStatus = "NEW" | "RECORDING" | "DIAGNOSIS" | "%future added value";
export type PatientTableQuery$variables = {};
export type PatientTableQuery$data = {
  readonly allPatients: ReadonlyArray<{
    readonly id: string;
    readonly sex: PatientSex;
    readonly birthday: string;
    readonly concern: string;
    readonly admissionDate: string;
    readonly status: PatientStatus;
  }>;
};
export type PatientTableQuery = {
  variables: PatientTableQuery$variables;
  response: PatientTableQuery$data;
};

const node: ConcreteRequest = (function(){
var v0 = [
  {
    "alias": null,
    "args": null,
    "concreteType": "Patient",
    "kind": "LinkedField",
    "name": "allPatients",
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
    "argumentDefinitions": [],
    "kind": "Fragment",
    "metadata": null,
    "name": "PatientTableQuery",
    "selections": (v0/*: any*/),
    "type": "Query",
    "abstractKey": null
  },
  "kind": "Request",
  "operation": {
    "argumentDefinitions": [],
    "kind": "Operation",
    "name": "PatientTableQuery",
    "selections": (v0/*: any*/)
  },
  "params": {
    "cacheID": "f43ef46183af19d560e781fba8b94e99",
    "id": null,
    "metadata": {},
    "name": "PatientTableQuery",
    "operationKind": "query",
    "text": "query PatientTableQuery {\n  allPatients {\n    id\n    sex\n    birthday\n    concern\n    admissionDate\n    status\n  }\n}\n"
  }
};
})();

(node as any).hash = "6d58e1b6fe4f2ff60e471bec73d554f0";

export default node;
