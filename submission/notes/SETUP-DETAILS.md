# Setup details

## Prerequisites and import details

For a smooth setup, have Switch Console, your chat workspace and a signed-in coding provider ready first. Then one template creates the three-agent team and its shared room.

1. [Install Switch Console](https://docs.switchagents.ai/switch-rooms/getting-started/install-switch-console), add a server, and sign in to your coding provider. Use Python 3.11+; this project needs no packages.
2. Obtain this checkout. Create a fresh starting copy with `python3 scripts/prepare_rehearsal.py ../promise-rehearsal`. The destination must be new and outside this project; the exporter in it deliberately leaks extra columns. Keep all agents on that copy.
3. Connect Slack or Discord through Switch and invite a second person to review the export. You request it; they provide independent sign-off. Use both participants' actual account names. See [chat setup](https://docs.switchagents.ai/switch-rooms/getting-started/index).
4. In Console **Templates → Import template**, paste [switch-room.template.yaml](../../switch-room.template.yaml), save, then **Use template**. Choose a unique team prefix, connected bridge, actual requester/approver, online machine, installed provider and the **same absolute rehearsal directory for every agent**. Enable server agent management where required by [the template guide](https://docs.switchagents.ai/switch-rooms/administer/room-templates). Select **Create all**. One run creates three agents and their room, and posts a kickoff; importing alone only saves the template.
5. Check both humans joined, all three agents can read the folder, and the coordinator can resolve actual authors/message refs and create its room documents. Paste the ordered messages from [DEMO.md](../../DEMO.md). Priya must inspect the actual file before approving. Missing context or permissions must stop the run.

The template uses `addressing: anyone` so both people and the agents can collaborate directly in the room. Use a dedicated team room for this workflow.

