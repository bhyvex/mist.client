import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate

def tunnel_action(args):
    client = authenticate()
    if args.action == 'list-tunnels':
        list_tunnels(client, args.pretty)
    elif args.action == 'add-tunnel':
        add_tunnel(client, args)
        print 'Tunnel %s to %s added successfully' % (args.name, args.cidrs)
    elif args.action == 'edit-tunnel':
        edit_tunnel(client, args)
        print 'Tunnel %s was edited successfully' % args.tunnel_id
    elif args.action == 'delete-tunnel':
        client.delete_tunnel(args.tunnel_id)
        print 'Tunnel %s removed' % args.tunnel_id


def list_tunnels(client, pretty):
    tunnels = client.list_tunnels()
    if not tunnels:
        print 'Could not find any VPN Tunnels found'
        sys.exit(0)
    if pretty:
        x = PrettyTable(['Name', 'ID', 'CIDRs', 'Description'])
        for tunnel in tunnels:
            x.add_row([tunnel['name'], tunnel['id'], tunnel['cidrs'], tunnel['description']])
        print x
    else:
        for tunnel in tunnels:
            print '%-40s %-40s %-40s %-40s' % (tunnel['name'], tunnel['id'],
                                               tunnel['cidrs'], tunnel['description'])


def add_tunnel(client, args):
    name = args.name
    cidrs = [cidr.strip(' ') for cidr in str(args.cidrs).split(',')]
    client_addr = args.client_arg
    description = args.description

    client.add_tunnel(name=name, cidrs=cidrs, client_addr=client_addr,
                      description=description)


def edit_tunnel(client, args):
    tunnel_id = args.tunnel_id
    name = args.name
    cidrs = [cidr.strip(' ') for cidr in str(args.cidrs).split(',')]
    description = args.description

    client.edit_tunnel(tunnel_id=tunnel_id, name=name, cidrs=cidrs,
                       description=description)


