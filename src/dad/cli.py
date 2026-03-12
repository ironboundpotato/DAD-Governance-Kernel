import json
import argparse

from dad.kernel import DADKernel
from dad.types import ActionRequest


def main():
    parser = argparse.ArgumentParser(
        description="D.A.D. Governance Kernel CLI"
    )

    parser.add_argument(
        "--authority",
        required=True,
        help="Authority ID requesting the action"
    )

    parser.add_argument(
        "--action",
        required=True,
        help="Action being requested"
    )

    parser.add_argument(
        "--context",
        default="{}",
        help="JSON context for evaluation"
    )

    args = parser.parse_args()

    context = json.loads(args.context)

    kernel = DADKernel()

    request = ActionRequest(
        authority_id=args.authority,
        action=args.action,
        context=context
    )

    result = kernel.evaluate(request)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()