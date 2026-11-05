# Setup details

## Prerequisites and import details

The five-minute target starts with Console, a connected chat workspace and a signed-in coding provider ready. A cold installation or agent response time can take longer.

1. [Install Switch Console](https://docs.switchagents.ai/switch-rooms/getting-started/install-switch-console), add a server, and sign in to your coding provider. Use Python 3.11+; this project needs no packages.
2. Obtain this checkout. Create a fresh starting copy with `python3 scripts/prepare_rehearsal.py ../promise-rehearsal`. The destination must be new and outside this project; the exporter in it deliberately leaks extra columns. Keep all agents on that copy.
3. Connect a real Slack or Discord workspace through Switch and invite a second person. You play Sam; they play Priya. Use their actual usernames, not the character names unless those are their accounts. See [chat setup](https://docs.switchagents.ai/switch-rooms/getting-started/index). The bridge must be connected before the template can create its room.
4. In Console **Templates → Import template**, paste [switch-room.template.yaml](../../switch-room.template.yaml), save, then **Use template**. Choose a unique team prefix, connected bridge, actual requester/approver, online machine, installed provider and the **same absolute rehearsal directory for every agent**. Enable server agent management where required by [the template guide](https://docs.switchagents.ai/switch-rooms/administer/room-templates). Select **Create all**. One run creates three agents and their room, and posts a kickoff; importing alone only saves the template.
5. Check both humans joined, all three agents can read the folder, and the coordinator can resolve actual authors/message refs and create its room documents. Paste the ordered messages from [DEMO.md](../../DEMO.md). Priya must inspect the actual file before approving. Missing context or permissions must stop the run.

The template uses `addressing: anyone` so the second room member and agents can address each other. Keep this a dedicated room with trusted participants.

