import discord
import config

localization = config.localization['npc_model']


class CharacterInfo:

    def __init__(self, npc_dict, current_year, color):
        self.profile = npc_dict
        self.year = current_year
        self.sort_key = self.profile['names'].get('surname', "zzz")
        self.secondary_sort_key = self.profile['names'].get('firstname', "zzz")
        self.color_value = color

    def __str__(self):
        return self.get_name()

    def get_name(self):
        names = self.profile["names"]
        title = names.get("title", None)
        first_name = names.get("firstname", None)
        middle_name = names.get("middle", None)
        if middle_name:
            middle_name = self.alter_possible_list_to_string(middle_name, lambda x: "{}.".format(x[0]))
        nickname = names.get("nickname", None)
        if nickname:
            nickname = self.alter_possible_list_to_string(nickname, lambda x: '"{}"'.format(x))
        surname = names.get("surname", None)
        moniker = names.get("moniker", None)
        name_list = filter(None, [title, first_name, middle_name, nickname, surname])
        full_name = " ".join(name_list)
        if full_name and moniker:
            return "{}, {}".format(full_name, moniker)
        elif full_name:
            return full_name
        elif moniker:
            return moniker
        return "-"

    @staticmethod
    def alter_possible_list_to_string(list_candidate, alter_function):
        if type(list_candidate) == list:
            alter_list = []
            for item in list_candidate:
                alter_list.append(alter_function(item))
            return " ".join(alter_list)
        else:
            return alter_function(list_candidate)

    def get_organizations(self):
        organizations = self.profile.get("organization", None)
        if not organizations:
            return []
        memberships = []
        if type(organizations) != list:
            organizations = [organizations]
        for organization in organizations:
            org_name = organization.get("name")
            rank = organization.get("rank", localization['default_rank'])
            status = organization.get("status", "")
            if status:
                status += " "
            memberships.append(localization['org_format'].format(status, rank, org_name))
        return memberships

    def get_race(self):
        subrace = self.profile.get("subrace", "")
        if subrace:
            subrace = "({}) ".format(subrace)
        race = subrace + self.profile.get("race", "-")
        return race

    def get_profession(self):
        profession = self.profile.get("class", "-")
        if type(profession) == list:
            return ", ".join(profession)
        else:
            return profession

    def get_age(self):
        if "birthyear" in self.profile:
            if "deathyear" in self.profile and int(self.profile["deathyear"]) < self.year:
                age = int(self.profile["deathyear"]) - int(self.profile["birthyear"])
                return "{} ({} - {})".format(age, self.profile["birthyear"], self.profile["deathyear"])
            elif int(self.profile["birthyear"]) > self.year:
                return "-"
            else:
                age = self.year - int(self.profile["birthyear"])
                return age
        else:
            return "-"

    def get_npc_embed(self):
        embed = discord.Embed(title=self.get_name(),
                              description=self.profile.get("description", ""),
                              color=self.color_value)

        embed.add_field(name=localization['gender'], value=self.profile.get("gender", "-"), inline=True)
        embed.add_field(name=localization['age'], value=self.get_age(), inline=True)
        embed.add_field(name=localization['location'], value=self.profile.get("location", "-"), inline=True)

        embed.add_field(name=localization['race'], value=self.get_race(), inline=True)
        embed.add_field(name=localization['class'], value=self.get_profession(), inline=True)

        organizations = self.get_organizations()
        new_orgs = ["● {}".format(x) for x in organizations]
        organization_string = "\n".join(new_orgs)
        if not organization_string:
            organization_string = "-"

        embed.add_field(name=localization['organization'], value=organization_string, inline=False)

        return embed
