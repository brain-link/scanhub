/**
 * @generated SignedSource<<b1874d72cfaa60762e599182b1425471>>
 * @lightSyntaxTransform
 * @nogrep
 */

/* tslint:disable */
/* eslint-disable */
// @ts-nocheck

import { ConcreteRequest, Query } from 'relay-runtime';
export type DeviceTableQuery$variables = {};
export type DeviceTableQuery$data = {
  readonly allDevices: ReadonlyArray<{
    readonly id: string;
    readonly modality: string;
    readonly address: string;
    readonly site: {
      readonly name: string;
      readonly city: string;
    } | null;
  }>;
};
export type DeviceTableQuery = {
  variables: DeviceTableQuery$variables;
  response: DeviceTableQuery$data;
};

const node: ConcreteRequest = (function(){
var v0 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "id",
  "storageKey": null
},
v1 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "modality",
  "storageKey": null
},
v2 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "address",
  "storageKey": null
},
v3 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "name",
  "storageKey": null
},
v4 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "city",
  "storageKey": null
};
return {
  "fragment": {
    "argumentDefinitions": [],
    "kind": "Fragment",
    "metadata": null,
    "name": "DeviceTableQuery",
    "selections": [
      {
        "alias": null,
        "args": null,
        "concreteType": "Device",
        "kind": "LinkedField",
        "name": "allDevices",
        "plural": true,
        "selections": [
          (v0/*: any*/),
          (v1/*: any*/),
          (v2/*: any*/),
          {
            "alias": null,
            "args": null,
            "concreteType": "Site",
            "kind": "LinkedField",
            "name": "site",
            "plural": false,
            "selections": [
              (v3/*: any*/),
              (v4/*: any*/)
            ],
            "storageKey": null
          }
        ],
        "storageKey": null
      }
    ],
    "type": "Query",
    "abstractKey": null
  },
  "kind": "Request",
  "operation": {
    "argumentDefinitions": [],
    "kind": "Operation",
    "name": "DeviceTableQuery",
    "selections": [
      {
        "alias": null,
        "args": null,
        "concreteType": "Device",
        "kind": "LinkedField",
        "name": "allDevices",
        "plural": true,
        "selections": [
          (v0/*: any*/),
          (v1/*: any*/),
          (v2/*: any*/),
          {
            "alias": null,
            "args": null,
            "concreteType": "Site",
            "kind": "LinkedField",
            "name": "site",
            "plural": false,
            "selections": [
              (v3/*: any*/),
              (v4/*: any*/),
              (v0/*: any*/)
            ],
            "storageKey": null
          }
        ],
        "storageKey": null
      }
    ]
  },
  "params": {
    "cacheID": "2848944c7c39051dcff49f04ddfc4a88",
    "id": null,
    "metadata": {},
    "name": "DeviceTableQuery",
    "operationKind": "query",
    "text": "query DeviceTableQuery {\n  allDevices {\n    id\n    modality\n    address\n    site {\n      name\n      city\n      id\n    }\n  }\n}\n"
  }
};
})();

(node as any).hash = "2a260d74af864fbb86d83401fbbb71d2";

export default node;
