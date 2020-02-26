from aws_cdk import aws_ec2
from aws_cdk.aws_ec2 import ISecurityGroup, IPeer


class SecurityGroupModifier:
    def __init__(self, security_group: ISecurityGroup):
        self.__security_group = security_group

    def open_port(self, port: int, peer: IPeer, ingress: bool = True) -> None:
        sg = self.__security_group
        if ingress:
            sg.add_ingress_rule(
                peer=peer,
                connection=aws_ec2.Port(
                    protocol=aws_ec2.Protocol.TCP,
                    string_representation=f'Ingress {port} rule for {sg.security_group_id}.',
                    from_port=port,
                    to_port=port
                )
            )
        else:
            sg.add_egress_rule(
                peer=peer,
                connection=aws_ec2.Port(
                    protocol=aws_ec2.Protocol.TCP,
                    string_representation=f'Egress {port} rule for {sg.security_group_id}.',
                    from_port=port,
                    to_port=port
                )
            )