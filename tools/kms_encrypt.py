#!/usr/bin/env python

import argparse
import base64

import boto3


def encrypt(session, secret: str, alias: str):
    return base64.b64encode(
        session.client("kms").encrypt(
            KeyId=alias,
            Plaintext=secret.encode("utf8"),
        )["CiphertextBlob"]
    ).decode("utf8")


def create_argument_parser():
    parser = argparse.ArgumentParser(description="Encrypt a string using a KMS key")
    parser.add_argument(
        "-k", "--key", metavar="keyId", required=True, help="the KMS key ID"
    )
    parser.add_argument(
        "-f",
        "--file",
        metavar="path",
        required=True,
        help="path to the file with the string to be encrypted",
    )
    return parser


if __name__ == "__main__":
    args = create_argument_parser().parse_args()
    with open(args.file, "r") as file:
        text = file.read().strip()

    aws_session = boto3.Session()
    ciphertext = encrypt(aws_session, text, args.key)
    print(ciphertext)
