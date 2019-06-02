import discord


class CharacterInfo:

    def __init__(self, npc_dict, current_year):
        self.profile = npc_dict
        self.year = current_year
        self.sort_key = self.profile['names'].get('surname', "")
        self.secondary_sort_key = self.profile['names'].get('first', "")

    def __str__(self):
        return self.get_name()

    def get_name(self):
        names = self.profile["names"]
        title = names.get("title", None)
        first_name = names.get("first", None)
        middle_name = names.get("middle", None)
        if middle_name:
            if type(middle_name) == list:
                new_middle_name = ""
                for name in middle_name:
                    new_middle_name += "{}.".format(name)
                middle_name = new_middle_name
            else:
                middle_name = "{}.".format(middle_name[0])
        nickname = names.get("nickname", None)
        if nickname:
            nickname = '"{}"'.format(nickname)
        surname = names.get("surname", None)
        monnicker = names.get("monnicker", None)
        name_list = filter(None, [title, first_name, middle_name, nickname, surname])
        full_name = " ".join(name_list)
        if full_name and monnicker:
            return "{}, {}".format(full_name, monnicker)
        elif full_name:
            return full_name
        elif monnicker:
            return monnicker
        return "-"

    def get_organizations(self):
        organizations = self.profile.get("organization", None)
        if not organizations:
            return []
        memberships = []
        if type(organizations) != list:
            organizations = [organizations]
        for organization in organizations:
            org_name = organization.get("name")
            rank = organization.get("rank", "Member")
            status = organization.get("status", "")
            if status:
                status += " "
            memberships.append("{}{} of the {}.".format(status, rank, org_name))
        return memberships

    def get_race(self):
        subrace = self.profile.get("subrace", "")
        if subrace:
            subrace = "({}) ".format(subrace)
        race = subrace + self.profile.get("race", "-")
        return race

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
        embed = discord.Embed(title=self.get_name(), description=self.profile.get("description", ""), color=16744512)

        embed.add_field(name="Gender", value=self.profile.get("gender", "-"), inline=True)
        embed.add_field(name="Age", value=self.get_age(), inline=True)
        embed.add_field(name="Location", value=self.profile.get("location", "-"), inline=True)

        embed.add_field(name="Race", value=self.get_race(), inline=True)
        embed.add_field(name="Class", value=self.profile.get("class", "-"), inline=True)

        organizations = self.get_organizations()
        new_orgs = ["● {}".format(x) for x in organizations]
        organization_string = "\n".join(new_orgs)
        if not organization_string:
            organization_string = "-"

        embed.add_field(name="Organizations", value=organization_string, inline=False)

        return embed
