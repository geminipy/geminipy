# -*- coding: utf-8 -*-

class Networks:
    _NETWORKS = {
        'gusd': 'gusd',
        'btc': 'bitcoin',
        'eth': 'ethereum',
        'bch': 'bitcoincash',
        'ltc': 'litecoin',
        'zec': 'zcash',
        'fil': 'filecoin',
        'doge': 'dogecoin',
        'xtz': 'tezos'
    }

    @classmethod
    def get_network(cls, term):
        term = str(term).lower()
        if term in cls._NETWORKS or term in cls._NETWORKS.values():
            return cls._NETWORKS[term] if term in cls._NETWORKS else term
        else:
            raise ValueError(f'Network for coin "{term} is not supported.')

    @classmethod
    def get_coin_network(cls, network):
        network = str(network).lower()
        if network not in cls._NETWORKS.values():
            raise ValueError(f'Network  "{network}" is not supported.')
        for k, v in cls._NETWORKS.items():
            if network == v:
                return k

    @classmethod
    def get_networks(cls):
        return list(cls._NETWORKS.values())
