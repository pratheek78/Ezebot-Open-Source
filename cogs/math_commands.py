import discord
from sympy import *
import math as math 

from discord.ext import commands 
from typing import Optional   



class MathCom(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def calc(self, ctx, op, prob1, prob2: Optional[float], prob3: Optional[float]):
        if op == "round":
            fprob = float(prob1)
            sol = math.ceil(fprob)
            await ctx.send(sol)

        elif op == "absolute":
            fprob = float(prob1)
            sol = math.fabs(fprob)
            await ctx.send(sol)

        elif op == "factorial":
            fprob = float(prob1)
            sol = math.factorial(fprob)
            await ctx.send(sol)

        elif op == "floor":
            fprob = float(prob1)
            sol = math.floor(fprob)
            await ctx.send(sol) 

        elif op == "hcf":
            iprob = int(prob1)
            iprob2 = int(prob2) #Converted both variables to integers, since the gcd mathod requires integers and nothing else matters(yes, i used bad grammar here intentionally for mettalica reference "hehe")
            sol = math.gcd(iprob, iprob2)
            await ctx.send(sol)

        elif op == "lcm":
            fprob = int(prob1)
            fprob2 = int(prob2) #Same as the above
            sol = math.lcm(fprob, fprob2)
            await ctx.send(sol)

        elif op == "exp":
            fprob = float(prob1)
            sol = math.exp(fprob)
            await ctx.send(sol)

        elif op == "power":
            fprob = float(prob1)
            fprob2 = float(prob2)
            sol = math.pow(fprob, fprob2)
            await ctx.send(sol)

        elif op == "sqrt":
            fprob = float(prob1)
            sol = math.sqrt(fprob)
            await ctx.send(sol)

        elif op == "acos": #Was going to add full trigonometry but got bored so ignore dis kek
            fprob = float(prob1)
            sol = math.acos(fprob)
            await ctx.send(sol)
        
        elif op == "radians":
            fprob = float(prob1)
            sol = math.radians(fprob)
            await ctx.send(sol)

        elif op == "degrees":
            fprob = float(prob1)
            sol = math.degrees(fprob)
            await ctx.send(sol)
        

    @commands.command()
    async def equation(self, eqn):
        pass



        

        
def setup(client):
    client.add_cog(MathCom(client))
        